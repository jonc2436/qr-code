from qr_code_generator.encode import *
import pytest


@pytest.mark.parametrize("data, expected", [
    ("1234", "0001"),
    ("ASHDJENS", "0010"),
    ("123bd123", "0100"),
    ("lkamef@#*$(!@#)()dfald213", "0100"),
    ("https://www.qrcode.com/", "0100"),
])
def test_get_mode_indicator(data, expected):
    assert get_mode_indicator(data) == expected


@pytest.mark.parametrize("count, mode, err_corr, expected", [
    (23, "0100", "M", 2),
    (41, "0001", "L", 1),
    (42, "0001", "L", 2),
])
def test_get_minimum_size(count, mode, err_corr, expected):
    assert get_minimum_size(count, mode, err_corr) == expected


@pytest.mark.parametrize("data, mode, expected", [
    ("1234", "0001", 4),
    ("HELLO WORLD", "0010", 11),
    ("é" * 8, "0100", 16),
])
def test_get_character_count(data, mode, expected):
    assert get_character_count(data, mode) == expected


@pytest.mark.parametrize("count, mode, version, expected", [
    (11, "0010", 1, "000001011"),
    (11, "0010", 10, "00000001011"),
    (11, "0010", 27, "0000000001011"),
])
def test_get_character_count_indicator(count, mode, version, expected):
    assert get_character_count_indicator(count, mode, version) == expected


@pytest.mark.parametrize("data, expected", [
    ("HELLO WORLD", "0110000101101111000110100010111001011011100010011010100001101"),
    ("0", "000000"),
    ("9", "001001"),
    ("A", "001010"),
    ("Z", "100011"),
    (" ", "100100"),
    (":", "101100"),
    ("00", "00000000000"),
    ("01", "00000000001"),
    ("10", "00000101101"),
    ("::", "11111101000"),
    ("A0", "00111000010"),
    ("0A", "00000001010"),
    ("$%", "11010100111"),
    ("*+", "11100000011"),
    ("-.", "11101011111"),
    ("/:", "11110111011"),
    ("ABC", "00111001101001100"),
    ("000", "00000000000000000"),
    ("A00", "00111000010000000"),
    (" A", "11001011110"),
    ("A ", "00111100110"),
    ("  ", "11001111000"),
    (" A ", "11001011110100100"),
    ("0123456789", "0000000000100001011101000101110010010001010100101110001"),
    ("OPENAI", "100010100010101000110100111010100"),
    ("A1B2C3", "001110000110011111000101000011111"),
    ("HELLO WORLD ", "011000010110111100011010001011100101101110001001101010001001101101"),
    (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:",
        "0000000000100001011101000101110010010001010100101110001001110011"
        "0101000101001010100001010101110000101100111101011100110010111111"
        "0101100010100011001010110110100001001101011001011011100000111000"
        "01110111001111001110110101011110011000111110001101101100"
    ),
])
def test_encode_alphanumeric(data, expected):
    assert encode_alphanumeric(data) == expected


@pytest.mark.parametrize("data, version, err_corr, expected", [
    ("1" * 104, 1, "Q", "1" * 104),
    ("1" * 102, 1, "Q", "1" * 102 + "00"),
    ("1" * 99, 1, "Q", "1" * 99 + "00000"),
    ("1" * 92, 1, "Q", "1" * 92 + "000011101100"),
    ("1" * 84, 1, "Q", "1" * 84 + "00001110110000010001"),
    ("1" * 74, 1, "Q", "1" * 74 + "000000111011000001000111101100"),
])
def test_pad_bytes(data, version, err_corr, expected):
    assert pad_bytes(data, version, err_corr) == expected
