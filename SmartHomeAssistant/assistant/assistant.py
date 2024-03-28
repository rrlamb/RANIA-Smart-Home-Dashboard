import os
import geocoder

import google.generativeai as genai
import google.generativeai.types
import speech_recognition as sr
import whisper
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from datetime import date
from pocketsphinx import Decoder, Config


# Load environment variables
load_dotenv()

# Get the location based on ip
_location = geocoder.ip('me')

# Initialize DuckDuckGo search
_search = DuckDuckGoSearchRun()

# Initialize recognizer and Whisper model
_recognizer = sr.Recognizer()
_microphone = sr.Microphone(sample_rate=16000)
_whisper_model = whisper.load_model("tiny")

# Initialize pocketsphinx decoder
_decoder = Decoder(Config(dict="./hotwords/hotwords.dict", keyphrase="hey rania"))

# Configure LLM
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
_llm_model = genai.GenerativeModel("gemini-1.0-pro-latest")
_conversation = _llm_model.start_chat(history=[])


def speech_to_text(recognizer: sr.Recognizer, audio: {}) -> str:
    try:
        return recognizer.recognize_whisper(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"


def listen_wake_word() -> bool:
    if _microphone.stream is None:
        _microphone.__enter__()

    stream = _microphone.stream.pyaudio_stream

    print('Say "Hey Rania"')
    _decoder.start_utt()

    while True:
        buf = stream.read(1024, exception_on_overflow=False)

        if buf:
            _decoder.process_raw(buf, False, False)
        else:
            print(f'An error has occured. Buf is: {buf}')
            return False

        if _decoder.hyp():
            _decoder.end_utt()
            return True


def listen() -> str:
    with sr.Microphone() as source:
        _recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Listening:")

        try:
            audio = _recognizer.listen(source, timeout=8)

            print("Processing speech to text...")

            # Save local audio
            with open("microphone.wav", "wb") as f:
                f.write(audio.get_wav_data())

            # Transcribe the spoken words from the user
            result = _whisper_model.transcribe("microphone.wav")

            return result['text']
        except sr.WaitTimeoutError:
            print("Timed out waiting for speech")

    return "Nothing was spoken"


def send_query(query: str) -> None | google.generativeai.types.GenerateContentResponse:
    prompt = f'''
        You will receive a query that you must answer as good as possible.
        Your answer will be based on the current date, location, conversation
        history, and what you know.
    
        The current date is {date.today().strftime('%A, %B %d, %Y')}.
    
        The location is {_location.address}.
    
        Here are the results of a DuckDuckGo search: ${_search.run(f'{query}')}
    
        Using what you know and these results respond to the message below.
        If the DuckDuckGo search does not provide enough information you may
        ignore the results and give an answer using other messages from this
        conversation. Do not mention the DuckDuckGo at all in your response
        in any way and respond as concisely as possible while still using
        full sentences.
    
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
    
        Query: ${query}'''

    try:
        # TODO: Adjust permission level. It is currently set to allow all
        return _conversation.send_message(prompt, stream=True, safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        })
    except Exception as e:
        # TODO: Improve error handling
        print(e)

    return None
