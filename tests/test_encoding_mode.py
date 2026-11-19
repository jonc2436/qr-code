from qr_code_generator.encoding_mode import encoding_mode
import pytest

@pytest.mark.parametrize("input, expected", [
    ("1234", "0001"),
    ("ASHDJENS", "0010"),
    ("123bd123", "0100"),
    ("lkamef@#*$(!@#)()dfald213", "0100"),
    ("https://www.qrcode.com/", "0100")
])

def test_encoding_mode(input : str, expected : str):
    assert encoding_mode(input) == expected