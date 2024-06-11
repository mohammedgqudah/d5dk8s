def chunk(_list, chunk_size):
    return [_list[i:i + chunk_size] for i in range(0, len(_list), chunk_size)]
