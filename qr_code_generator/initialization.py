from capacities import QR_CAPACITIES

NUMERIC = set("0123456789")
ALPHANUMERIC = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:")

def encoding_mode(data : str) -> str:
    if not data:
        raise ValueError("Empty Input")

    output = "0001"

    for char in data:
        if char in NUMERIC:
            continue
        elif char in ALPHANUMERIC:
            output = "0010"
        else:
            output = "0100"
            break

    return output

def get_minimum_size(err_corr : str, enc_mode : str, char_len : int) -> int:
    for key, values in QR_CAPACITIES.values():
        if values[err_corr][enc_mode] >= char_len:
            return key