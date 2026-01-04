import pytest
from qr_code.gf_functions import xtime

@pytest.mark.parametrize("input, expected", [
    (0x01, 0x02),
    (0x80, 0x1D),
    (0x8E, 0x01)
])

def test_xtime(input, expected):
    assert xtime(input) == expected