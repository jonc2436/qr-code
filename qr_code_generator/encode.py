from .lookup_tables.capacities import QR_CAPACITIES
from .lookup_tables.error_correction import QR_ERROR_CORRECTION
from .lookup_tables.character_count import QR_CHARACTER_COUNT_BITS
from .lookup_tables.alpha_encoding import ALPHANUMERIC_VALUES

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

def get_minimum_size(data : str, err_corr : str) -> int:
    if not isValid_err_corr(err_corr):
        raise ValueError("Error Correction is not valid")

    char_len = len(data)
    enc_mode = get_mode_indicator(data)
    
    for key, values in QR_CAPACITIES.items():
        if values[err_corr][enc_mode] >= char_len:
            return key

def get_character_count_indicator(data : str, err_corr : str) -> str:
    enc_mode = get_mode_indicator(data)
    size = get_minimum_size(data, err_corr)

    count_bit_len = 0

    if size >= 1 and size <= 9:
        count_bit_len = QR_CHARACTER_COUNT_BITS["1-9"][enc_mode]
    elif size <= 26:
        count_bit_len = QR_CHARACTER_COUNT_BITS["10-26"][enc_mode]
    elif size <= 40:
        count_bit_len = QR_CHARACTER_COUNT_BITS["27-40"][enc_mode]

    char_count_indicator = bin(len(data))[2:]

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