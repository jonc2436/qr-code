from .lookup_tables.capacities import QR_CAPACITIES
from .lookup_tables.error_correction import QR_ERROR_CORRECTION
from .lookup_tables.character_count import QR_CHARACTER_COUNT_BITS

NUMERIC = set("0123456789")
ALPHANUMERIC = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:")

def isValid_size(size : int) -> bool:
    return (size >= 1 and size <= 40) 

def isValid_err_corr(err_corr : str) -> bool:
    return (err_corr in set(["L", "M", "Q", "H"]))

def isValid_enc_mode(enc_mode : str) -> bool:
    return (enc_mode in set(["0001", "0010", "0100", "1000"]))

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
    if not isValid_err_corr(err_corr):
        raise ValueError("Error Correction is not valid")
    if not isValid_enc_mode(enc_mode):
            raise ValueError("Encoding Mode is not valid")
    
    for key, values in QR_CAPACITIES.items():
        if values[err_corr][enc_mode] >= char_len:
            return key

def get_num_codewords(size : int, err_corr : str) -> int:
    if not isValid_size(size):
        raise ValueError("Size is not valid")
    if not isValid_err_corr(err_corr):
        raise ValueError("Error Correction is not valid")

    return QR_ERROR_CORRECTION[size][err_corr]["total_data_codewords"]

def char_count_size(size : int, enc_mode : str) -> int:
    if not isValid_size(size):
        raise ValueError("Size is not valid")
    if not isValid_enc_mode(enc_mode):
        raise ValueError("Encoding Mode is not valid")

    if size >= 1 and size <= 9:
        return QR_CHARACTER_COUNT_BITS["1-9"][enc_mode]
    elif size <= 26:
        return QR_CHARACTER_COUNT_BITS["10-26"][enc_mode]
    elif size <= 40:
        return QR_CHARACTER_COUNT_BITS["27-40"][enc_mode]
