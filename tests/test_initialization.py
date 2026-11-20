from qr_code_generator.initialization import *
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