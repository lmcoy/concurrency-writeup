# just a simple python example
# out of the box no concurrency, parallelism or asynchrony

def square(x):
    return x * x

if __name__ == "__main__":
    print(f"square(2) = {square(2)}")