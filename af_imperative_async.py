"""
async yield syntax is not available yet
"""

import asyncio


async def schedule_iterable():
    prev = None
    while True:
        await asyncio.sleep(0.5)
        content = open('/sys/class/thermal/thermal_zone0/temp').read().strip()
        if prev == content:
            continue

        print(content)
        prev = content


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_iterable())
    loop.run_forever()


if __name__ == '__main__':
    main()
