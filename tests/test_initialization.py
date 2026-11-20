from qr_code_generator.encode import *
import pytest

@pytest.mark.parametrize("data, expected", [
    ("1234", "0001"),
    ("ASHDJENS", "0010"),
    ("123bd123", "0100"),
    ("lkamef@#*$(!@#)()dfald213", "0100"),
    ("https://www.qrcode.com/", "0100")
])

def test_get_mode_indicator(data, expected):
    assert get_mode_indicator(data) == expected

@pytest.mark.parametrize("data, err_corr, expected", [
    ("https://www.qrcode.com/", "M", 2)
])

def test_get_minimum_size(data, err_corr, expected):
    assert get_minimum_size(data, err_corr) == expected

@pytest.mark.parametrize("data, err_corr, expected", [
    ("HELLO WORLD", "Q", "000001011")
])

def test_get_character_count_indicator(data, err_corr, expected):
    assert get_character_count_indicator(data, err_corr) == expected

@pytest.mark.parametrize("data, expected", [
    ("HELLO WORLD", "0110000101101111000110100010111001011011100010011010100001101"),
    pytest.param("0", "000000", id="single-zero"),
    pytest.param("9", "001001", id="single-digit"),
    pytest.param("A", "001010", id="single-letter"),
    pytest.param("Z", "100011", id="single-z"),
    pytest.param(" ", "100100", id="single-space"),
    pytest.param(":", "101100", id="single-colon"),
    pytest.param("00", "00000000000", id="zero-pair"),
    pytest.param("01", "00000000001", id="pair-with-leading-zero"),
    pytest.param("10", "00000101101", id="reversed-digit-pair"),
    pytest.param("::", "11111101000", id="maximum-pair"),
    pytest.param("A0", "00111000010", id="letter-digit"),
    pytest.param("0A", "00000001010", id="digit-letter"),
    pytest.param("$%", "11010100111", id="dollar-percent"),
    pytest.param("*+", "11100000011", id="asterisk-plus"),
    pytest.param("-.", "11101011111", id="hyphen-period"),
    pytest.param("/:", "11110111011", id="slash-colon"),
    pytest.param("ABC", "00111001101001100", id="odd-length-letters"),
    pytest.param("000", "00000000000000000", id="odd-length-zeros"),
    pytest.param("A00", "00111000010000000", id="zero-at-odd-tail"),
    pytest.param(" A", "11001011110", id="leading-space"),
    pytest.param("A ", "00111100110", id="trailing-space"),
    pytest.param("  ", "11001111000", id="two-spaces"),
    pytest.param(" A ", "11001011110100100", id="spaces-around-letter"),
    pytest.param(
        "0123456789",
        "0000000000100001011101000101110010010001010100101110001",
        id="all-digits",
    ),
    pytest.param("OPENAI", "100010100010101000110100111010100", id="even-length-letters"),
    pytest.param("A1B2C3", "001110000110011111000101000011111", id="mixed-letters-digits"),
    pytest.param(
        "HELLO WORLD ",
        (
            "0110000101101111000110100010111001011011100010011010100010011011"
            "01"
        ),
        id="even-length-with-trailing-space",
    ),
    pytest.param(
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:",
        (
            "0000000000100001011101000101110010010001010100101110001001110011"
            "0101000101001010100001010101110000101100111101011100110010111111"
            "0101100010100011001010110110100001001101011001011011100000111000"
            "01110111001111001110110101011110011000111110001101101100"
        ),
        id="all-supported-characters",
    ),
])

def test_encode_alphanumeric(data, expected):
    assert encode_alphanumeric(data) == expected
