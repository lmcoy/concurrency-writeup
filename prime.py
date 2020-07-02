import trio

async def generate_int(channel):
    """generate_int writes all integers >= 2 ordered into `channel`"""
    i = 2
    while True:
        await channel.send(i)
        i += 1

async def filter_div_by(in_channel, out_channel, prime):
    """filter_div_by reads all elements from `in_channel` and 
    writes them to `out_channel` if the element is not divisible by `prime`."""
    while True:
        value = await in_channel.receive()
        if value % prime != 0:
            await out_channel.send(value)

async def print_first_n_primes(n):
    int_ch_send, int_ch_recv = trio.open_memory_channel(0)
    async with trio.open_nursery() as nursery:
        # fill channel with all integers >= 2
        nursery.start_soon(generate_int, int_ch_send)
        ch_recv = int_ch_recv
        for i in range(n):
            prime = await ch_recv.receive() # get the next prime
            print(prime)
            filtered_ch_send, filtered_ch_recv = trio.open_memory_channel(0)
            # create a new task that processes all elements from `ch_recv` and puts
            # all received elements that are not divisible by `prime` into `filtered_ch_send`.
            nursery.start_soon(filter_div_by, ch_recv, filtered_ch_send, prime)
            # in next iteration read from filtered channel
            ch_recv = filtered_ch_recv
        nursery.cancel_scope.cancel() # all done, cancel tasks

# create a chain of filters:
# after 3 was processed:  filter_div_by(2) | filter_div_by(3)
# put 4 > filter_div_by(2) | filter_div_by(3)
#       4 is consumed by `filter_div_by(2)` but discarded, i.e. filter chain has no output
# put 5 > filter_div_by(2) | filter_div_by(3)
#       5 survives filters, `prime` is set to 5 and printed
#       filter chain is updated to: filter_div_by(2) | filter_div_by(3) | filter_div_by(5)
#       let for loop listen to updated filter chain

trio.run(print_first_n_primes, 10)
