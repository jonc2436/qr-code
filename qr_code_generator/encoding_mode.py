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

