import os

def get_dict_from_csv(filename: str) -> list:
    result: list = []
    keys: list = []
    with open(f'./data/{filename}', 'r') as reader:
        lines = reader.readlines()
        is_first_line: bool = True
        for line in lines:
            if is_first_line:
                keys = line.split(',')
                is_first_line = False
            else:
                values = line.split(',')
                item = dict(zip(keys, values))
                result.append(item)
    return result
    
