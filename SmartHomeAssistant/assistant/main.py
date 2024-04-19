import json
import websockets
import pyttsx3

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
                    # Windows
                    engine = pyttsx3.init()
                    engine.say(responseJson["response"]["text"])
                    engine.runAndWait()
                    # Mac & Linux
                    # engine = pyttsx3.init()
                    # engine.say(response.txt)
                    # engine.runAndWait()
                    print(responseJson["response"]["text"])

                    await websocket.send(
                        json.dumps(
                            {
                                "text": responseJson["response"]["text"],
                                "route": "/",
                                "waittime": 2,
                            }
                        )
                    )


if __name__ == "__main__":
    run(producer)
