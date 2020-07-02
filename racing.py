import trio, random, time

async def race(n, *async_fns):
    """race starts all `*async_fns` and returns the result of the first `n` tasks
    that finish. All losing tasks are cancelled."""
    # channels are a way for communication of concurrent taks
    # this is how tasks interact which each other.
    send_channel, receive_channel = trio.open_memory_channel(0) # create channel with no buffer
    async def sender(async_fn):
        # await the result of `async_fn`, once it is available put it into channel.
        # `send` only finishes when value is added to channel. If something is in channel
        #  it will wait until channel is empty and put it then.
        await send_channel.send(await async_fn) 
    
    async with trio.open_nursery() as nursery:
        for async_fn in async_fns:
            nursery.start_soon(sender, async_fn)  # start all `async_fn`
        # get n first elements from channel. receives waits until an element is available
        winner = [await receive_channel.receive() for i in range(n)]
        nursery.cancel_scope.cancel() # we have our winners, cancel all the losers
        return winner

async def fn(i):
    await trio.sleep(random.randint(1, 3600)) # sleep up to 1h
    print(i) # print who I am
    return i

async def main():
    start_time =  time.perf_counter()
    result = await race(5, *[fn(i) for i in range(7200)]) # 7200 tasks!!!
    print(f"execution time = {time.perf_counter() - start_time}")
    print(result)
    await trio.sleep(60) # wait to see that all coroutines started by `race` are cancelled and not printing

trio.run(main)
