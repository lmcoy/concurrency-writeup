import trio, random, math

async def retry(max_tries, async_fn):
    """retry runs the task `async_fn` up to `max_tries` times. 
    It returns its result in case of success (first run without an exception raised) or raises
    an exception when all `max_tries` runs raised an exception.

    retry uses an exponential backoff with jitter between the retries.
    """
    if max_tries <= 0:
        raise ValueError("max_tries must be greater than 0")
    
    async def go(n, it):
        try:
            return await f()
        except Exception as ex:
            if n > 1:
                tmp = 2**(it-1)
                await trio.sleep(tmp + random.uniform(0, tmp))
                return  await go(n - 1, it+1)
            else:
                raise Exception(f"failure after {it+1} tries", ex)
    await go(max_tries, 0)
    
async def f():
    print(".", end='') # print . and no line break
    if (random.randint(0,1) == 1): # f fails in 50% of calls
        raise Exception("exception")

async def main():
    with trio.move_on_after(30): # run program for 30 seconds
        while True:
            await retry(10, f)
            print("|")

trio.run(main)
