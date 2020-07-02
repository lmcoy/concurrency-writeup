import trio

async def forever(async_fn, *args):
    """
    forever is equivalent to infinite loop that executes `async_fn` forever.
    """
    while True:
        await async_fn(*args)
        await trio.sleep(0)  # insert checkpoint in case async_fn has no checkpoint
        # trio uses cooperative multitasking/scheduling: tasks have to yield control.
        # If trio.sleep(0) is not called (and async_fn does not contain anything that
        # yields control), the trio runtime will never get control again and this task
        # will run forever without any concurrency, i.e. the timeout in main is never used. 
        
async def aprint(x):
    # note: this function is obviously not useful and serves only as a minimal  example
    print(x)

async def main():
    # timeout task after 3 seconds
    with trio.move_on_after(3):
        await forever(aprint, "hello")

trio.run(main)
