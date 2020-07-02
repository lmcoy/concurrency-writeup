import trio, time

async def benchmark(f, x):
    """benchmark awaits the async function `f(x)`, prints the execution time and returns the result."""
    start_time = time.perf_counter()
    result = await f(x)
    print(f"execution time: {time.perf_counter() - start_time} s")
    return result

async def square(x):
    # new keywords `async` and `await` (python >= 3.5)
    # `await` can only be used in `async` functions.
    await trio.sleep(4) # wait 4 seconds (just to do something asynchronous)
    return x * x

if __name__ == "__main__":
    coroutine = square(2) # calling async functions creates only coroutine object
    print(f"square(2) = {coroutine}")
    # special runner function to run async function in sync functions.
    # (We cannot call async functions in normal sync functions directly.)
    # `run` is an event loop orchestrating `async` tasks/functions
    result = trio.run(benchmark, square, 2) # run benchmark(square, 2)
    print(f"run square(2)  = {result}")
