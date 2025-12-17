import pytest
from qr_code.encoder import get_version, encode_alphanumeric, encode_data

@pytest.mark.parametrize("mode,text_length,err_corr,expected", [
    ("Alphanumeric", 11, "Q", 1),
    ("Alphanumeric", 18, "Q", 2),
    ("Alphanumeric", 16, "Q", 1),
    ("Alphanumeric", 17, "Q", 2),
    ("Alphanumeric", 29, "Q", 2),
    ("Alphanumeric", 30, "Q", 3),
    ("Alphanumeric", 1, "L", 1),
    ("Alphanumeric", 25, "L", 1),
    ("Alphanumeric", 26, "L", 2),
    ("Alphanumeric", 855, "Q", 23),
    ("Alphanumeric", len("HELLO THERE WORLD"), "Q", 2)
])

def test_get_version(mode, text_length, err_corr, expected):
    assert get_version(mode, text_length, err_corr) == expected

@pytest.mark.parametrize("text,expected", [
    ("HELLO WORLD", "0110000101101111000110100010111001011011100010011010100001101"),
    ("AB", "00111001101"),
    ("CODE-39", "010001101000100101011111100111000001001"),
    ("AC-42", "0011100111011100111001000010")
])

def test_encode_alphanumeric(text, expected):
    assert encode_alphanumeric(text) == expected

def test_encode_data():
    assert encode_data("HELLO WORLD", "Alphanumeric", "M") == "00100000010110110000101101111000110100010111001011011100010011010100001101000000111011000001000111101100000100011110110000010001"

encode_data("HELLO WORLD", "Alphanumeric", "Q", True)