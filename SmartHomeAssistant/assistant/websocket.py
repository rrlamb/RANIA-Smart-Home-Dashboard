import asyncio
import websockets


async def consumer(message: str) -> None:
    # do something with the message
    print(message)


async def producer() -> str:
    message = "Hello, World!"
    # print('sending message')
    await asyncio.sleep(1)
    return message


async def consumer_handler(websocket: websockets.WebSocketServerProtocol) -> None:
    async for message in websocket:
        await consumer(message)


async def producer_handler(websocket: websockets.WebSocketServerProtocol) -> None:
    while True:
        message = await producer()
        await websocket.send(message)


async def handler(websocket: websockets.WebSocketServerProtocol) -> None:
    consumer_task = asyncio.create_task(consumer_handler(websocket))
    producer_task = asyncio.create_task(producer_handler(websocket))

    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    for task in pending:
        task.cancel()


async def serve(host: str, port: int) -> None:
    # TODO: add encryption
    async with websockets.serve(handler, host, port):
        await asyncio.Future()


def run() -> None:
    asyncio.run(serve(host="", port=8001))


if __name__ == "__main__":
    run()
