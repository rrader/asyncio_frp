"""
async yield syntax is not available yet
"""

import asyncio


async def poll_file(path):
    """
    Events source.
    :param path: file path to poll
    :param delay: periodic polling delay
    """
    while True:
        content = open(path).read().strip()
        async yield content


async def tick(delay):
    """
    Timer event source. Returns 1 every `delay` seconds
    :param delay: period in seconds
    """
    while True:
        await asyncio.sleep(delay)
        async yield 1


async def stream_zip(*streams):
    """
    Returns tuples of values from all streams
    :param in_: input Queue
    """
    while True:
        l = []
        for i in streams:  # TODO: rewrite async
            l.append(await i.__anext__())
        async yield tuple(l)


async def distinct(in_):
    """
    Behavior that filters out sequences of equal values and yields just one.
    :param in_: input Queue
    """
    prev = None
    while True:
        value = await in_.__anext__()
        if value == prev:
            continue

        async yield value
        prev = value


async def print_stream(in_):
    """
    Behavior that prints all values.
    :param in_: input Queue
    """
    while True:
        value = await in_.__anext__()
        print(value)


async def schedule_iterable(iterable):
    async for _ in iterable:
        pass


def main():
    loop = asyncio.get_event_loop()
    async_generator = print_stream( distinct( stream_zip(tick(0.5), poll_file('/sys/class/thermal/thermal_zone0/temp')) ) )
    loop.create_task(schedule_iterable(async_generator))
    loop.run_forever()


if __name__ == '__main__':
    main()
