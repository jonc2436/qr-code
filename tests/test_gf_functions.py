import pytest
from qr_code.gf_functions import *

@pytest.mark.parametrize("a, expected", [
    (0x01, 0x02),
    (0x80, 0x1D),
    (0x8E, 0x01)
])

def test_xtime(a, expected):
    assert xtime(a) == expected

@pytest.mark.parametrize("a, b, expected", [
    (0x01, 0, 0),
    (0x01, 1, 0x01),
    (2, 0x8E, 1),
    (0x80, 0x02, 0x1D),
    (0x80, 0x03, 0x9D),
    (0xFF, 0x02, 0xE3),
    (0xC3, 0x02, 0x9B)
])

def test_mul(a, b, expected):
    assert mul(a, b) == expected