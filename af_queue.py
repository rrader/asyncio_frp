import asyncio


async def poll_file(out_, path):
    """
    Events source.
    :param out_: Queue object of output stream
    :param path: file path to poll
    :param delay: periodic polling delay
    """
    while True:
        content = open(path).read().strip()
        await out_.put(content)


async def tick(out_, delay):
    """
    Timer event source. Returns 1 every `delay` seconds
    :param out_: output Queue
    :param delay: period in seconds
    """
    while True:
        await asyncio.sleep(delay)
        await out_.put(1)


async def stream_zip(*streams, out_):
    """
    Returns tuples of values from all streams
    :param in_: input Queue
    :param out_: stream if distinct values
    """
    while True:
        l = []
        for i in streams:  # TODO: rewrite async
            l.append(await i.get())
        await out_.put(tuple(l))


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
    q_temp = asyncio.Queue(maxsize=1)
    q_ticks = asyncio.Queue()
    q_zip = asyncio.Queue()
    q1, q2 = asyncio.Queue(), asyncio.Queue()
    loop.create_task(poll_file(q_temp, '/sys/class/thermal/thermal_zone0/temp'))
    loop.create_task(tick(q_ticks, 0.5))
    loop.create_task(stream_zip(q_ticks, q_temp, out_=q_zip))
    loop.create_task(distinct(q_zip, q1))
    loop.create_task(print_stream(q1, q2))
    loop.run_forever()


if __name__ == '__main__':
    main()
