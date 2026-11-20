from .lookup_tables.capacities import QR_CAPACITIES
from .lookup_tables.character_count import QR_CHARACTER_COUNT_BITS
from .lookup_tables.alpha_encoding import ALPHANUMERIC_VALUES
from .lookup_tables.error_correction import QR_ERROR_CORRECTION

NUMERIC = set("0123456789")
ALPHANUMERIC = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:")

def isValid_err_corr(err_corr : str) -> bool:
    return (err_corr in set(["L", "M", "Q", "H"]))

def get_mode_indicator(data : str) -> str:
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

def get_character_count(data : str, mode : str) -> int:
    """Count UTF-8 bytes in byte mode, or characters in the other modes."""
    if mode == "0100":
        return len(data.encode("utf-8"))
    return len(data)

def get_minimum_size(count : int, mode : str, err_corr : str) -> int:
    if not isValid_err_corr(err_corr):
        raise ValueError("Error Correction is not valid")
    if count < 0:
        raise ValueError("Character count must be non-negative")

    for version, values in QR_CAPACITIES.items():
        if values[err_corr][mode] >= count:
            return version

    raise ValueError("Data does not fit in QR versions 1-40")

def get_character_count_indicator(count : int, mode : str, version : int) -> str:
    if not 1 <= version <= 40:
        raise ValueError("Version must be between 1 and 40")

    if version <= 9:
        count_bit_len = QR_CHARACTER_COUNT_BITS["1-9"][mode]
    elif version <= 26:
        count_bit_len = QR_CHARACTER_COUNT_BITS["10-26"][mode]
    else:
        count_bit_len = QR_CHARACTER_COUNT_BITS["27-40"][mode]

    if not 0 <= count < (1 << count_bit_len):
        raise ValueError("Character count does not fit in the count indicator")

    char_count_indicator = bin(count)[2:]

    while len(char_count_indicator) < count_bit_len:
        char_count_indicator = "0" + char_count_indicator

    return char_count_indicator

def encode_alphanumeric(data : str) -> str:
    encoded_str = ""

    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            total = 45*ALPHANUMERIC_VALUES[data[i]] + ALPHANUMERIC_VALUES[data[i+1]]

            cur_str = bin(total)[2:]

            while len(cur_str) < 11:
                cur_str = "0" + cur_str

            encoded_str += cur_str
            continue
        else:
            cur_str = bin(ALPHANUMERIC_VALUES[data[i]])[2:]

            while len(cur_str) < 6:
                cur_str = "0" + cur_str

            encoded_str += cur_str

    return encoded_str

def pad_bytes(encoded_str : str, version : int, err_corr : str) -> str:
    """Return the complete data bit string, including terminator and padding."""
    capacity_bits = QR_ERROR_CORRECTION[version][err_corr]["total_data_codewords"] * 8
    remaining_bits = capacity_bits - len(encoded_str)

    if remaining_bits < 0:
        raise ValueError("Encoded data exceeds the selected version's data capacity")

    encoded_final = encoded_str + "0" * min(4, remaining_bits)

    if len(encoded_final) % 8 != 0:
        encoded_final += "0" * (8 - (len(encoded_final) % 8))

    padding_values = ("11101100", "00010001")
    pad_index = 0
    while len(encoded_final) < capacity_bits:
        encoded_final += padding_values[pad_index]
        pad_index = 1 - pad_index

    return encoded_final
