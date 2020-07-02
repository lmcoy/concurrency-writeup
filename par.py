import trio, random

async def par(num_worker, *async_fns):
    """par runs all tasks in `async_fns` but only `num_worker` concurrently."""
    # create work permit channel with space for `num_worker` work permits
    send_channel, receive_channel = trio.open_memory_channel(num_worker)
    for i in range(num_worker):
        # put `num_worker` work permits into channel
        await send_channel.send(1)

    async def work(async_fn):
        await receive_channel.receive() # get a work permit from channel
        await async_fn # once work permit is available, work
        await send_channel.send(1) # return work permit

    async with trio.open_nursery() as nursery:
        for async_fn in async_fns:
            nursery.start_soon(work, async_fn) # start all async_fn

async def f(i):
    print(" "*i + '^')
    await trio.sleep(random.uniform(0, 5))
    print(" "*i + 'v')

async def main():
    await par(3, *[f(i) for i in range(10)])

trio.run(main)
