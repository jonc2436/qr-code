from lookup_tables.error_correction import QR_ERROR_CORRECTION
from gf_functions import *

def split_blocks(data : str, version : int, err_corr : str) -> dict:
    final_dict = {"block1": [], "block2":  []}

    group1_block_count = QR_ERROR_CORRECTION[version][err_corr]["group1_blocks"]
    group2_block_count = QR_ERROR_CORRECTION[version][err_corr]["group2_blocks"]

    if group1_block_count:
        block1_num_codewords = QR_ERROR_CORRECTION[version][err_corr]["group1_data_codewords_per_block"]

        for block_index in range(group1_block_count):
            block = []
        
            for codeword_index in range(block1_num_codewords):
                left = block_index*block1_num_codewords*8+codeword_index*8
                right = left + 8
                block.append(data[left:right])

            final_dict["block1"].append(block)

    if group2_block_count:
        block2_num_codewords = QR_ERROR_CORRECTION[version][err_corr]["group2_data_codewords_per_block"]
        offset = group1_block_count * block1_num_codewords * 8

        for block_index in range(group2_block_count):
            block = []
        
            for codeword_index in range(block2_num_codewords):
                left = offset+block_index*block2_num_codewords*8+codeword_index*8
                right = left + 8
                block.append(data[left:right])

            final_dict["block2"].append(block)
    
    return final_dict

def generate_polynomial(version : int, err_corr : str) -> list[int]:
    codewords_num = QR_ERROR_CORRECTION[version][err_corr]["ec_codewords_per_block"]
    first_poly = [1, 1]

    for i in range(1, codewords_num):
        second_poly = [1, antilog[i]]
        first_poly_len, second_poly_len = len(first_poly), len(second_poly)
        product = [0]*(first_poly_len + second_poly_len - 1)

        for poly_x in range(first_poly_len):
            for poly_y in range(second_poly_len):
                product[poly_x+poly_y] ^= gf_multiply(first_poly[poly_x], second_poly[poly_y])

        first_poly = product

    return product