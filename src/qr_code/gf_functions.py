def xtime(a : int) -> int:
    top_bit = (a >> 7) & 0x1
    new_bits = (a << 1) & 0xFF

    if top_bit == 1:
        new_bits ^= 0x1D
    
    return new_bits

def mul(a : int, b : int) -> int:
    new_bits = 0

    while b != 0:
        if b & 1:
            new_bits ^= a
        
        a = xtime(a)
        b >>= 1

    return new_bits