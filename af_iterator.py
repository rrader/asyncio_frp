import asyncio


class FilePoller:
    def __init__(self, path):
        self.path = path

    async def __aiter__(self):
        return self

    async def __anext__(self):
        content = open(self.path).read().strip()
        return content


class Zip:
    def __init__(self, *inputs):
        self.inputs = inputs

    async def __aiter__(self):
        return self

    async def __anext__(self):
        l = []
        for i in self.inputs:  # TODO: rewrite async
            l.append(await i.__anext__())
        return tuple(l)


class Tick:
    def __init__(self, delay):
        self.delay = delay

    async def __aiter__(self):
        return self

    async def __anext__(self):
        await asyncio.sleep(self.delay)
        return 1


class Distinct:
    def __init__(self, input):
        self.input = input
        self.prev = None

    async def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            val = await self.input.__anext__()
            if self.prev != val:
                break
        self.prev = val
        return val


class Printer:
    def __init__(self, input):
        self.input = input

    async def __aiter__(self):
        return self

    async def __anext__(self):
        val = await self.input.__anext__()
        print(val)


async def process_stream():
    stream = Printer( Distinct( Zip( Tick(0.5), FilePoller('/sys/class/thermal/thermal_zone0/temp') ) ) )
    async for i in stream:
        pass


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_stream())


if __name__ == '__main__':
    main()
