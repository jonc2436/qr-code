# Log and anti-log tables
log = [None]*256
antilog = [None]*255
value = 1

for exponent in range(255):
    if exponent == 0:
        log[value] = exponent
        antilog[exponent] = value
    else:
        value <<= 1

        if value >= 256:
            value ^= 285

        log[value] = exponent
        antilog[exponent] = value

def gf_multiply(x : int, y : int) -> int:
    if x == 0 or y == 0:
        return 0

    return antilog[(log[x] + log[y]) % 255]

def gf_divide(x : int, y : int) -> int:
    return antilog[(log[x] - log[y]) % 255]