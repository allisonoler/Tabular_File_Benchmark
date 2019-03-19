import mmap

def getColIndicesToQuery(col_names_file_path, memory_map):
    with open(col_names_file_path, "rb") as col_file:
        if memory_map:
            col_file = mmap.mmap(col_file.fileno(), 0, prot=mmap.PROT_READ)
            index_range = [int(line.rstrip(b"\n").split(b"\t")[0]) for line in iter(col_file.readline, b"")]
        else:
            index_range = [int(line.rstrip(b"\n").split(b"\t")[0]) for line in col_file]

    col_file.close()

    return index_range

def getColNamesToQuery(col_names_file_path, memory_map):
    with open(col_names_file_path, "rb") as col_file:
        if memory_map:
            col_file = mmap.mmap(col_file.fileno(), 0, prot=mmap.PROT_READ)
            col_names = [line.rstrip(b"\n").split(b"\t")[1] for line in iter(col_file.readline, b"")]
        else:
            col_names = [line.rstrip(b"\n").split(b"\t")[1] for line in col_file]

    col_file.close()

    return col_names

def parse_data_coords(line_indices, coords_file, coords_file_max_length, full_str_length):
    coords_file_length = len(coords_file)
    out_dict = {}

    for index in line_indices:
        start_pos = index * (coords_file_max_length + 1)
        next_start_pos = start_pos + coords_file_max_length + 1
        further_next_start_pos = min(next_start_pos + coords_file_max_length, coords_file_length)

        if start_pos in out_dict:
            data_start_pos = out_dict[start_pos]
        else:
            data_start_pos = int(coords_file[start_pos:next_start_pos].rstrip())

        if next_start_pos == further_next_start_pos:
            data_end_pos = full_str_length
        else:
            if next_start_pos in out_dict:
                data_end_pos = out_dict[next_start_pos]
            else:
                data_end_pos = int(coords_file[next_start_pos:further_next_start_pos].rstrip())

        yield [index, data_start_pos, data_end_pos]

def parse_data_values(start_offset, segment_length, data_coords, str_like_object, end_offset=0):
    start_pos = start_offset * segment_length

    for coords in data_coords:
        yield str_like_object[(start_pos + coords[1]):(start_pos + coords[2] + end_offset)].rstrip()

def buildStringMap(the_list):
    # Find maximum length of value
    max_value_length = max([len(str(x)) for x in set(the_list)])

    # Build output string
    output = b""
    formatter = "{:<" + str(max_value_length) + "}\n"
    for value in the_list:
        output += formatter.format(value).encode()

    return output, str(max_value_length).encode()

def readIntFromFile(file_path, file_extension):
    with open(file_path + file_extension, 'rb') as the_file:
        return int(the_file.read().rstrip())

def openReadFile(file_path, file_extension):
    the_file = open(file_path + file_extension, 'rb')
    return mmap.mmap(the_file.fileno(), 0, prot=mmap.PROT_READ)
