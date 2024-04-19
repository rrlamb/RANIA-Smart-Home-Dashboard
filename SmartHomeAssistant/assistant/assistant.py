import os
import geocoder
import subprocess
import json

import google.generativeai as genai
import google.generativeai.types
import speech_recognition as sr
from typing import Optional
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from datetime import date, datetime
from pocketsphinx import Decoder
from duckduckgo_search import DDGS


# Load environment variables
load_dotenv()

# Get the location based on ip
_location = geocoder.ip("me")

# Initialize DuckDuckGo search
# _search = DuckDuckGoSearchRun()


# Initialize recognizer and Whisper model
_recognizer = sr.Recognizer()
_microphone = sr.Microphone(sample_rate=16000)

# Initialize pocketsphinx decoder
# Specify the path to the keyword list file and dictionary
keyword_list_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "hotwords", "keyword_list.txt"
)
dict_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "hotwords", "hotwords.dict"
)

# Configuration parameters directly aimed at initializing with kws mode
config = {
    "dict": dict_path,
    "kws": keyword_list_path,
}

# Initialize the decoder with these specific settings aimed at kws mode
_decoder = Decoder(**config)


# Configure LLM
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
_llm_model = genai.GenerativeModel("gemini-1.0-pro-latest")
_conversation = _llm_model.start_chat(history=[])


def speech_to_text(audio: sr.AudioData) -> Optional[str]:
    try:
        return _recognizer.recognize_whisper(audio)
    except sr.UnknownValueError:
        return None


def listen_wake_word() -> bool:
    if _microphone.stream is None:
        _microphone.__enter__()

    print('Say "Hey Rania"')
    _decoder.start_utt()

    while True:
        buf = _microphone.stream.pyaudio_stream.read(1024, exception_on_overflow=False)

        if buf:
            _decoder.process_raw(buf, False, False)
        else:
            print(f"An error has occured. Buf is: {buf}")
            return False

        if _decoder.hyp() is not None:
            for seg in _decoder.seg():
                print(seg.word)
            _decoder.end_utt()
            return True


def listen() -> str:
    with sr.Microphone(sample_rate=16000) as source:
        print("Adjusting for ambient noise. Please wait...")
        _recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Listening for speech:")

        try:
            audio = _recognizer.listen(source, timeout=8)
            audio_file_path = "user_query.wav"
            with open(audio_file_path, "wb") as f:
                f.write(audio.get_wav_data())
            return audio_file_path
        except sr.WaitTimeoutError:
            print("Timed out waiting for speech")

    return None


def send_to_whisper(wav_file_path: str) -> Optional[str]:
    # path to whisper executable
    whisper_executable = "./whisper.cpp/main"

    # Call whisper.cpp with subprocess
    result = subprocess.run(
        [
            whisper_executable,
            "-m",
            "./whisper.cpp/models/ggml-tiny.en-q5_1.bin",
            "-oj",
            "-f",
            wav_file_path,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Error processing audio:", result.stderr)
        return None

    # Grab output JSON from whisper.cpp and parse it to extract
    # speech to text result
    try:
        with open("./user_query.wav.json", "r") as file:
            data = json.load(file)

        # Extract text from the first entry in the transcription array
        transcription_text = data.get("transcription", [{}])[0].get("text", None)
        return transcription_text
    except (IOError, json.JSONDecodeError) as e:
        print("Error reading or parsing JSON file: ", str(e))
        return None


def send_query(
    query: str,
) -> Optional[google.generativeai.types.GenerateContentResponse]:
    prompt = f"""
        You will receive a query that you must answer as effectively as possible.
        Your answer will be based on the current date, the current time, 
        location, conversation history, and the duckduckgo search.
    
        The current date is {date.today().strftime('%A, %B %d, %Y')}.
        The current time is {datetime.now().strftime('%H:%M')}.
    
        The location is {_location.address}.
    
        Here are the results of a DuckDuckGo search: ${DDGS().text(f'{query}', 
                                                                   max_results=1)[0]['title']}
        Using what you know and these results, respond to the message below.
        If the DuckDuckGo search does not provide enough information you may
        ignore the results and rely on other messages from this conversation to
        answer the query. Do not mention the DuckDuckGo at all in your response
        in any way.

        Aim to provide responses that are not only informative but also convey
        warmth and friendliness to the user. In your responses, prioritize 
        clarity and engagement, while also aiming to be concise
        with full sentences.

        When responding to queries that involve health or medical information,
        include a disclaimer urging the user to consult with a trained medical
        professional for personalized advice. This is to ensure the user's
        safety and to acknowledge your limitations in providing
        medical guidance.
    
        Format your response as JSON and structure it as shown below:
        {{
            "type": "answer" | "task" | "cancel",
            "response": {{
                "text": "Insert your answer to the query here if the type is set to answer",
            }}
        }}
    
        Set the type to answer if the user is asking you something or chatting conversationally.
        Set the type to task if the user is asking you to perform a task.
        Set the type to cancel if the user no longer wishes to continue the conversation.
        Examples of cancel would be "Nevermind", "Stop", or anything similar.
    
        Query: ${query}"""

    try:
        # TODO: Adjust permission level. It is currently set to allow all
        return _conversation.send_message(
            prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
        )
    except Exception as e:
        # TODO: Improve error handling
        print(e)

    return None
