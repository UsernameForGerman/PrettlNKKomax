import asyncio
import time

a = None

async def print_after(message, delay=1):
    """Print a message after the specified delay (in seconds)"""
    while a is None:
        await asyncio.sleep(delay)
        print('sleeping')
    else:
        return a

async def main():
    global a
    # Start coroutine twice (hopefully they start!)
    first_awaitable = asyncio.create_task(print_after("world!", 2))
    second_awaitable = asyncio.create_task(print_after("Hello", 1))

    # Wait for coroutines to finish
    print(await first_awaitable)
    print(await second_awaitable)


asyncio.run(main())