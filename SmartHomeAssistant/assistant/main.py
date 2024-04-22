import json
import websockets
from TTS.api import TTS
import pygame
import librosa
import time

from assistant import (
    listen_wake_word,
    listen,
    speech_to_text,
    send_query,
    send_to_whisper,
)
from websocket import run


async def producer(websocket: websockets.WebSocketServerProtocol) -> None:
    while True:
        if listen_wake_word():
            await websocket.send(json.dumps({"route": "/listening"}))

            audio = listen()

            if audio is not None:
                print("Processing speech to text...")
                await websocket.send(json.dumps({"route": "/response"}))

                query = send_to_whisper(audio)
                print(f"Asking: {query}")
                response = None

                if query is None:
                    # TODO: Respond with error message
                    print("Could not understand")
                else:
                    response = send_query(query)

                if response is not None:
                    responseJson = json.loads(response.text)
                    tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")
                    tts.tts_to_file(text=responseJson["response"]["text"])
                    # Windows
                    # engine = pyttsx3.init()
                    # engine.say(responseJson["response"]["text"])
                    # engine.runAndWait()
                    # Mac & Linux
                    # engine = pyttsx3.init()
                    # engine.say(response.txt)
                    # engine.runAndWait()
                    print(responseJson["response"]["text"])
                    my_sound = pygame.mixer.Sound("output.wav")
                    my_sound.play()

                    await websocket.send(
                        json.dumps(
                            {
                                "text": responseJson["response"]["text"],
                                "route": "/",
                                "waittime": librosa.get_duration(filename="output.wav") + 3.0
                            }
                        )
                    )
                    time.sleep(librosa.get_duration(filename="output.wav") + 3.0)


if __name__ == "__main__":
    pygame.init()
    run(producer)
