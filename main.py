from qr_code_generator.encode import (
    encode_alphanumeric,
    get_character_count,
    get_character_count_indicator,
    get_minimum_size,
    get_mode_indicator,
    pad_bytes,
)


def build_data_bits(input_string : str, err_corr : str) -> str:
    mode_indicator = get_mode_indicator(input_string)
    count = get_character_count(input_string, mode_indicator)
    version = get_minimum_size(count, mode_indicator, err_corr)
    character_count_indicator = get_character_count_indicator(count, mode_indicator, version)

    match mode_indicator:
        case "0010":
            encoded_data = encode_alphanumeric(input_string)
        case _:
            raise NotImplementedError("Only alphanumeric payload encoding is implemented")

    data_bits = mode_indicator + character_count_indicator + encoded_data
    return pad_bytes(data_bits, version, err_corr)


if __name__ == "__main__":
    print(build_data_bits("HELLO WORLD", "Q"))