import os
import unicodecsv as csv


def find_common_keys(data):
    common_keys = set()
    for item in data:
        common_keys |= set(item.keys())
    return list(common_keys)

def write_json_array_to_csv(data, filename, append=False):
    if not append:
        with open(filename, 'wb') as f:
            w = csv.DictWriter(f, find_common_keys(data))
            w.writeheader()
            w.writerows(data)
    else:
        needs_header = not os.path.exists(filename)
        with open(filename, 'ab') as f:
            w = csv.DictWriter(f, find_common_keys(data))
            if needs_header:
                w.writeheader()
            w.writerows(data)

