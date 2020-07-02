import copy


class Vector2:
    """
    Vector2 implements a tuple of integers (x,y) with addition.

    This class assumes 32bit integers for illustration purpose.
    The value of x is stored in the upper 16 bits of a 32 bit integer.
    The value of y is stored in the lower 16 bits of a 32 bit integer.

    example:
    |------------ 32 bits --------------|
    |0110100101010|00000010010110|
    |---- x ----------| ---- y ----------|

    This example demonstrates how bit level operations can be done in parallel
    because the CPU needs only one `add` operation to add two integers.
    Think of SIMD (SSE) operations for real examples.
    """
    def __init__(self, x: int, y: int):
        if not (-32768 <= x <= 32767):
            raise ValueError("x out of range")
        if not (-16384 <= y <= 16383):
            # keep one bit free for possible overflows
            raise ValueError("y out of range")
        self._data = x << 0x10 | (y & 0x7FFF)
    
    def x(self) -> int:
        return self._data >> 0x10
    
    def y(self) -> int:
        r = self._data & 0x7FFF
        if 0x4000 & r:  # value is negative, i.e. two complement
            # convert from two complement in positive int, take only relevant bits, and make result negative
            return -((~(r - 1)) & 0x7FFF) 
        else:
             return r

    def __add__(self, o):
        """ add the vector: both components are added in parallel!"""
        s = copy.deepcopy(self)
        # the addition operation adds two integers in parallel
        s._data += o._data
        return s

    def __str__(self) -> str:
        return f"({self.x()},{self.y()})"


print(Vector2(32765, 16382) + Vector2(2, 1))
