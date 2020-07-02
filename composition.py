import trio, time
from simpletracer.tracer import Tracer

async def child(x):
    print(f"start {x}")
    await trio.sleep(5)
    print(f"finish {x}")

async def parent():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(child, 1)
        nursery.start_soon(child, 2)
        nursery.start_soon(child, 3)

async def heartbeat(c):
    """heartbeat prints `c` every 0.5 seconds forever."""
    while (True):
        print(c)
        await trio.sleep(0.5)

async def delay(delay, nursery, f, *args,):
    """delay first sleeps for `delay` seconds and then starts `f(*args)` on `nursery`."""
    await trio.sleep(delay)
    nursery.start_soon(f, *args) # `delay` is not responsible for `f`. The owner of `nursery` is

async def withHeartbeat(f, *args):
    """withHeartbeat runs `f(*args)` and prints `.` every 0.5 seconds while `f` is running."""
    async with trio.open_nursery() as nursery:
        nursery.start_soon(delay, 0.5, nursery, heartbeat, '.') # nursery can be passed as arg
        await f(*args)
        nursery.cancel_scope.cancel() # cancel all children in nursery, i.e. the delayed heartbeat

trio.run(withHeartbeat, parent, instruments=[])
