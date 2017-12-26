from __future__ import print_function, unicode_literals, division


def raw_data_reader(raw_data):
    with open(raw_data, b'rb') as binary_file:
        data = binary_file.read()
    return data
