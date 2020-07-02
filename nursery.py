import trio, time

async def child(x):
    """child is a task to be run concurrently."""
    print (f"start {x}")
    await trio.sleep(5)
    #time.sleep(5) # -- using this leads to not concurrent execution
    print(f"finish {x}")

async def parent():
    async with trio.open_nursery() as nursery:
        # nursery supervises all child tasks that it starts
        nursery.start_soon(child, 1) # spawn child 1 but do not wait for it to finish
        nursery.start_soon(child, 2)
        nursery.start_soon(child, 3)
        # at the end of `with`: wait for all children in nursery to exit (children cannot run away)

trio.run(parent)