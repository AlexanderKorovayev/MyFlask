import asyncio


async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    f.set_result('I have finished.')


fut = asyncio.Future()

print(fut.done())

# loop = asyncio.get_event_loop()
# loop.create_task(main(fut))
# loop.run_until_complete(fut)
asyncio.run(main(fut))

print(fut.done())
print(fut.result())
