from qr_code_generator.initialization import *
import pytest

@pytest.mark.parametrize("string, expected", [
    ("1234", "0001"),
    ("ASHDJENS", "0010"),
    ("123bd123", "0100"),
    ("lkamef@#*$(!@#)()dfald213", "0100"),
    ("https://www.qrcode.com/", "0100")
])

def test_encoding_mode(string, expected):
    assert encoding_mode(string) == expected

@pytest.mark.parametrize("err_corr, enc_mode, char_len, expected", [
    ("M", "0100", len("https://www.qrcode.com/".encode("utf-8")), 2),

    # A single character/byte fits in version 1 in every mode.
    ("L", "0001", 1, 1),
    ("M", "0010", 1, 1),
    ("Q", "0100", 1, 1),
    ("H", "1000", 1, 1),

    # Version 1 numeric limits: exact capacity fits; one more needs version 2.
    ("L", "0001", 41, 1),
    ("L", "0001", 42, 2),
    ("M", "0001", 34, 1),
    ("M", "0001", 35, 2),
    ("Q", "0001", 27, 1),
    ("Q", "0001", 28, 2),
    ("H", "0001", 17, 1),
    ("H", "0001", 18, 2),

    # Version 1 alphanumeric limits, at all four error correction levels.
    ("L", "0010", 25, 1),
    ("L", "0010", 26, 2),
    ("M", "0010", 20, 1),
    ("M", "0010", 21, 2),
    ("Q", "0010", 16, 1),
    ("Q", "0010", 17, 2),
    ("H", "0010", 10, 1),
    ("H", "0010", 11, 2),

    # Version 1 byte limits.
    ("L", "0100", 17, 1),
    ("L", "0100", 18, 2),
    ("M", "0100", 14, 1),
    ("M", "0100", 15, 2),
    ("Q", "0100", 11, 1),
    ("Q", "0100", 12, 2),
    ("H", "0100", 7, 1),
    ("H", "0100", 8, 2),

    # Version 1 Kanji limits (the lookup supports this mode directly).
    ("L", "1000", 10, 1),
    ("L", "1000", 11, 2),
    ("M", "1000", 8, 1),
    ("M", "1000", 9, 2),
    ("Q", "1000", 7, 1),
    ("Q", "1000", 8, 2),
    ("H", "1000", 4, 1),
    ("H", "1000", 5, 2),

    # Version 9 -> 10, where character-count indicator lengths change.
    ("L", "0001", 552, 9),
    ("L", "0001", 553, 10),
    ("M", "0010", 262, 9),
    ("M", "0010", 263, 10),
    ("Q", "0100", 130, 9),
    ("Q", "0100", 131, 10),
    ("H", "1000", 60, 9),
    ("H", "1000", 61, 10),

    # Version 26 -> 27, another character-count indicator boundary.
    ("L", "0001", 3283, 26),
    ("L", "0001", 3284, 27),
    ("M", "0010", 1542, 26),
    ("M", "0010", 1543, 27),
    ("Q", "0100", 751, 26),
    ("Q", "0100", 752, 27),
    ("H", "1000", 365, 26),
    ("H", "1000", 366, 27),

    # First length requiring version 40 and its exact maximum capacity.
    ("L", "0001", 6744, 40),
    ("L", "0001", 7089, 40),
    ("M", "0010", 3221, 40),
    ("M", "0010", 3391, 40),
    ("Q", "0100", 1580, 40),
    ("Q", "0100", 1663, 40),
    ("H", "1000", 751, 40),
    ("H", "1000", 784, 40)
])

def test_get_minimum_size(err_corr, enc_mode, char_len, expected):
    assert get_minimum_size(err_corr, enc_mode, char_len) == expected
