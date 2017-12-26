from __future__ import print_function, unicode_literals, division

from resources.protobufs.generated_proto import InstrumentRating_pb2, Meta_pb2


def meta_data_reader(meta_data):
    meta = Meta_pb2.Meta()
    with open(meta_data, b'rb') as proto_file:
        data = proto_file.read()
    meta.ParseFromString(data)
    return meta


def read_instrument_rating(data):
    with open(data, b'rb') as f:
        proto_file = f.read()
    instrument_rating = InstrumentRating_pb2.InstrumentRating()
    instrument_rating.ParseFromString(proto_file)
    return instrument_rating
