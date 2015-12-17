import asyncio


def source(coro):
    def _source(loop, *args, **kwargs):
        output_queue = asyncio.Queue(1)
        loop.create_task( coro(output_queue, *args, **kwargs) )
        return output_queue
    return _source


def behavior(coro):
    def _source(loop, *args, **kwargs):
        output_queue = asyncio.Queue()
        loop.create_task( coro(output_queue, *args, **kwargs) )
        return output_queue
    return _source


@source
async def poll_file(out_, path):
    """
    Events source.
    :param out_: Queue object of output stream
    :param path: file path to poll
    """
    while True:
        content = open(path).read().strip()
        await out_.put(content)


@source
async def tick(out_, delay):
    """
    Timer event source. Returns 1 every `delay` seconds
    :param out_: output Queue
    :param delay: period in seconds
    """
    while True:
        await asyncio.sleep(delay)
        await out_.put(1)


@behavior
async def stream_zip(out_, *streams):
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


@behavior
async def distinct(out_, in_):
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


@behavior
async def print_stream(out_, in_):
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
    values_stream = distinct(loop,
                             stream_zip(loop,
                                        tick(loop, 0.5),
                                        poll_file(loop, '/sys/class/thermal/thermal_zone0/temp') )
                             )
    print_stream(loop, values_stream)
    loop.run_forever()


if __name__ == '__main__':
    main()
