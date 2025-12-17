from .constants import QR_CAPACITY, ALPHANUMERIC_TABLE, MODE_INDICATOR, CHAR_COUNT_INDICATOR_BITS, ERROR_CORRECTION

# Returns the QR code version based on number of characters and level of error correction
def get_version(mode, char_length, err_corr):
    for version, value in QR_CAPACITY.items():
        if char_length <= value[err_corr][mode]:
            qr_version = version
            break

    return qr_version

# Function that generates the binary encoded data of the alphanumeric text
def encode_alphanumeric(text):
    text_len = len(text)
    encoded_data = ""

    # We want each pair of characters
    for i in range(0, text_len, 2):
        # When not the last character
        if i != text_len - 1:
            first_char_val = ALPHANUMERIC_TABLE[text[i]]
            second_char_val = ALPHANUMERIC_TABLE[text[i+1]]

            # Formula for finding the number representation for each pair of characters
            # Evaluated as (numeric rep of 1st char * 45) + (numeric rep of 2nd char)
            num_rep = first_char_val * 45 + second_char_val
            bin_rep = bin(num_rep)[2:]

            # Pad the left with 0s to get a 11-bit binary string
            if len(bin_rep) < 11:
                bin_rep = bin_rep.zfill(11)
        # When last character
        else:
            # Last character does not need any special calculations
            num_rep = ALPHANUMERIC_TABLE[text[i]]
            bin_rep = bin(num_rep)[2:]

            # Pad the left with 0s to get a 6-bit binary string
            if len(bin_rep) < 6:
                bin_rep = bin_rep.zfill(6)
        
        encoded_data += bin_rep
            
    return encoded_data

def encode_data(text, mode, err_corr, debug=False):
    char_length = len(text)

    qr_version = get_version(mode, char_length, err_corr)
    
    # First 4 bits of the encoded data based on mode
    mode_bits = MODE_INDICATOR[mode]

    # Finding the # of bits required to encode the character length of the text
    for version, bit_count in CHAR_COUNT_INDICATOR_BITS[mode].items():
        if qr_version <= version:
            char_count_bit_len = bit_count
            break

    char_count_bits = bin(char_length)[2:].zfill(char_count_bit_len)
    encoded_text_bits = encode_alphanumeric(text)

    final_bits = mode_bits + char_count_bits + encoded_text_bits

    # Adding terminator bits as necessary
    # Finding the total number of data bits that are required for this QR code version & error correction level
    total_bit_count = ERROR_CORRECTION[f'{qr_version}-{err_corr}']["total_data_codewords"] * 8
    if total_bit_count - len(final_bits) < 4:
        terminator_bits = "0" * (total_bit_count - len(final_bits))
    else:
        terminator_bits = "0" * 4

    # Addding pad bytes if the length of the encoded_text is not a multiple of 8
    if len(final_bits) % 8 != 0:
        final_bits += "0" * (8 - (len(final_bits) % 8))

    # Adding pad bytes if the length of the encoded_text does not fill max capacity
    # 11101100 00010001 is the specific set of bytes that must be added as pad bytes
    for i in range((total_bit_count - len(final_bits)) // 8):
        if i % 2 == 0:
            final_bits += "11101100"
        else:
            final_bits += "00010001"

    # Print Diagnostics
    if debug == True:
        print(f'Mode Indicator: {mode_bits}')
        print(f'Character Count Indicator: {char_count_bits}')
        print(f'Encoded Data Bits:')
        display_bits = ""
        for i in range(len(encoded_text_bits)):
            if i > 0 and i % 11 == 0:
                print(display_bits)
                display_bits = ""

            display_bits += encoded_text_bits[i]

        if len(display_bits) != 0:
            print(display_bits)

        print(f'Terminator Bits: {terminator_bits}')

        # Final Encoded Data
        display_bits = ""
        print("Final Output:", end=" ")
        for i in range(len(final_bits)):
            if i != 0 and i % 8 == 0:
                print(display_bits, end=" ")
                display_bits = ""

            display_bits += final_bits[i]

    return final_bits