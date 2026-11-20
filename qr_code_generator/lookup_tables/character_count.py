"""Character-count indicator widths in bits, from the supplied table.

Lookup: QR_CHARACTER_COUNT_BITS[version_range][mode_indicator].
Version ranges include both endpoints.
Modes: 0001 = numeric, 0010 = alphanumeric, 0100 = byte, 1000 = Kanji.
"""

QR_CHARACTER_COUNT_BITS: dict[str, dict[str, int]] = {
    "1-9": {"0001": 10, "0010": 9, "0100": 8, "1000": 8},
    "10-26": {"0001": 12, "0010": 11, "0100": 16, "1000": 10},
    "27-40": {"0001": 14, "0010": 13, "0100": 16, "1000": 12},
}
