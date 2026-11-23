from lookup_tables.error_correction import QR_ERROR_CORRECTION

def split_blocks(data : str, version : int, err_corr : str) -> dict:
    final_dict = {"block1": [], "block2":  []}

    group1_block_count = QR_ERROR_CORRECTION[version][err_corr]["group1_blocks"]
    group2_block_count = QR_ERROR_CORRECTION[version][err_corr]["group2_blocks"]

    if group1_block_count:
        block1_num_codewords = QR_ERROR_CORRECTION[version][err_corr]["group1_data_codewords_per_block"]

        for i in range(group1_block_count):
            final_dict["block1"].append([])

            for j in range(block1_num_codewords):
                final_dict["block1"][i].append(data[i*block1_num_codewords*8+j*8:i*block1_num_codewords*8+j*8+8])

    if group2_block_count:
        block2_num_codewords = QR_ERROR_CORRECTION[version][err_corr]["group2_data_codewords_per_block"]
        offset = group1_block_count * block1_num_codewords * 8

        for k in range(group2_block_count):
            final_dict["block2"].append([])

            for l in range(block2_num_codewords):
                final_dict["block2"][k].append(data[offset+k*block2_num_codewords*8+l*8:offset+k*block2_num_codewords*8+l*8+8])        
    
    return final_dict