import asyncio


async def poll_file(out_, path, delay=0.5):
    """
    Events source.
    :param out_: Queue object of output stream
    :param path: file path to poll
    :param delay: periodic polling delay
    """
    while True:
        await asyncio.sleep(delay)
        content = open(path).read().strip()
        await out_.put(content)


async def distinct(in_, out_):
    """
    Behavior that filters out sequences of equal values and yields just one.
    :param in_: input Queue
    :param out_: stream if distinct values
    """
    prev = None
    while True:
        value = await in_.get()
        if value == prev:
            continue

        await out_.put(value)
        prev = value


async def print_stream(in_, out_=None):
    """
    Behavior that prints all values.
    :param in_: input Queue
    :param out_: nothing
    """
    while True:
        value = await in_.get()
        print(value)


def main():
    loop = asyncio.get_event_loop()
    q = asyncio.Queue()
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()
    loop.create_task(poll_file(q, '/sys/class/thermal/thermal_zone0/temp'))
    loop.create_task(distinct(q, q1))
    loop.create_task(print_stream(q1, q2))
    loop.run_forever()


if __name__ == '__main__':
    main()
