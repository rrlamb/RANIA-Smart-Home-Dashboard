import asyncio
import websockets
import functools
from typing import Callable, Awaitable


async def _producer_handler(
    websocket: websockets.WebSocketServerProtocol,
    producer: Callable[[websockets.WebSocketServerProtocol], Awaitable[None]],
) -> None:
    while True:
        await producer(websocket)


async def _handler(
    websocket: websockets.WebSocketServerProtocol,
    producer: Callable[[websockets.WebSocketServerProtocol], Awaitable[None]],
) -> None:
    # This is formatted in a way that a consumer could easily be added
    producer_task = asyncio.create_task(_producer_handler(websocket, producer))

    done, pending = await asyncio.wait(
        [producer_task], return_when=asyncio.FIRST_COMPLETED
    )

    for task in pending:
        task.cancel()


async def _serve(
    host: str,
    port: int,
    producer: Callable[[websockets.WebSocketServerProtocol], Awaitable[None]],
) -> None:
    # TODO: add encryption
    async with websockets.serve(
        functools.partial(_handler, producer=producer), host, port
    ):
        await asyncio.Future()


def run(
    producer: Callable[[websockets.WebSocketServerProtocol], Awaitable[None]]
) -> None:
    asyncio.run(_serve("", 8001, producer))
