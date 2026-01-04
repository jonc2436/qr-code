def xtime(a : int) -> int:
    top_bit = (a >> 7) & 0x1
    new_bits = (a << 1) & 0xFF

    if top_bit == 1:
        new_bits = new_bits ^ 0x1D
    
    return new_bits