def rotate_left(x: int, n: bytes):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def rotate_right(x: int, n: bytes):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF
