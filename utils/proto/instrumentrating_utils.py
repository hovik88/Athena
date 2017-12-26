from __future__ import division, print_function, unicode_literals

import datetime
from utils.proto import meta_reader
from utils.proto import mapping_to_proto
from resources.protobufs.generated_proto.InstrumentRating_pb2 import InstrumentRating
from utils.io_handler.proto_io import read_instrument_rating


def populate_instrument_rating(meta_data):
    data_list = meta_reader.meta_data_parser(meta_data)
    instrument_rating_list = []
    for data in data_list:
        instrument_rating = InstrumentRating()
        identifier = instrument_rating.identifiers.add()
        identifier.id = data['Identifier']['id']
        identifier.id_type = data['Identifier']['id_type']
        if data['source'] == 'Moodys':
            mdy_rating_history = instrument_rating.mdy_rating_history.add()
            for rating in data['mdy_latest_rating']['rating']:
                instrument_rating.mdy_latest_rating.rating = mapping_to_proto.md_mapping(rating)
                mdy_rating_history.rating = mapping_to_proto.md_mapping(rating)
            for date_ in data['mdy_latest_rating']['as_of_date']:
                instrument_rating.mdy_latest_rating.as_of_date = date_
                mdy_rating_history.as_of_date = date_
        elif data['source'] == 'SnP':
            instrument_rating.snp_latest_rating.rating = mapping_to_proto.snp_mapping(
                data['snp_latest_rating']['rating'])
            instrument_rating.snp_latest_rating.as_of_date = data['snp_latest_rating']['as_of_date']
            snp_rating_history = instrument_rating.snp_rating_history.add()
            snp_rating_history.rating = mapping_to_proto.snp_mapping(
                data['snp_latest_rating']['rating'])
            snp_rating_history.as_of_date = data['snp_latest_rating']['as_of_date']
        elif data['source'] == 'Fitch':
            instrument_rating.fitch_latest_rating.rating = mapping_to_proto.fitch_mapping(
                data['fitch_latest_rating']['rating'])
            instrument_rating.fitch_latest_rating.as_of_date = (
                data['fitch_latest_rating']['as_of_date'])
            fitch_rating_history = instrument_rating.fitch_rating_history.add()
            fitch_rating_history.rating = mapping_to_proto.fitch_mapping(
                data['fitch_latest_rating']['rating'])
            fitch_rating_history.as_of_date = data['fitch_latest_rating']['as_of_date']
        instrument_rating_list.append(instrument_rating)
        del instrument_rating
    return instrument_rating_list


def populate_history(instrument_rating_data, meta_data):
    instrument_rating = read_instrument_rating(instrument_rating_data)
    md_instrument_date = instrument_rating.mdy_latest_rating.as_of_date
    md_instrument_rating = instrument_rating.mdy_latest_rating.rating
    snp_instrument_date = instrument_rating.snp_latest_rating.as_of_date
    snp_instrument_rating = instrument_rating.snp_latest_rating.rating
    fitch_instrument_date = instrument_rating.fitch_latest_rating.as_of_date
    fitch_instrument_rating = instrument_rating.fitch_latest_rating.rating
    if md_instrument_date:
        dt = datetime.datetime.strptime(md_instrument_date, '%Y-%m-%d')
        rating = md_instrument_rating
    elif snp_instrument_date:
        dt = datetime.datetime.strptime(snp_instrument_date, '%Y-%m-%d')
        rating = snp_instrument_rating
    elif fitch_instrument_date:
        dt = datetime.datetime.strptime(fitch_instrument_date, '%Y-%m-%d')
        rating = fitch_instrument_rating
    else:
        dt = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')
        rating = ''
    data_list = meta_reader.meta_data_parser(meta_data)
    data = [data for data in data_list
            if instrument_rating.identifiers[0].id == data['Identifier']['id']][0]
    if data['source'] == 'Moodys':
        dt_raw = datetime.datetime.strptime(data['mdy_latest_rating']['as_of_date'], '%Y-%m-%d')
        rating_raw = data['mdy_latest_rating']['rating']
        if rating_raw != rating:
            if dt_raw > dt:
                ratings = instrument_rating.mdy_rating_history.add()
                ratings.rating = mapping_to_proto.md_mapping(rating_raw)
                ratings.as_of_date = dt_raw.strftime('%Y-%m-%d')
    elif data['source'] == 'SnP':
        dt_raw = datetime.datetime.strptime(data['snp_latest_rating']['as_of_date'], '%Y-%m-%d')
        rating_raw = data['snp_latest_rating']['rating']
        if rating_raw != rating:
            if dt_raw > dt:
                ratings = instrument_rating.snp_rating_history.add()
                ratings.rating = mapping_to_proto.snp_mapping(rating_raw)
                ratings.as_of_date = dt_raw.strftime('%Y-%m-%d')
    elif data['source'] == 'Fitch':
        dt_raw = datetime.datetime.strptime(data['fitch_latest_rating']['as_of_date'], '%Y-%m-%d')
        rating_raw = data['fitch_latest_rating']['rating']
        if rating_raw != rating:
            if dt_raw > dt:
                ratings = instrument_rating.fitch_rating_history.add()
                ratings.rating = mapping_to_proto.fitch_mapping(rating_raw)
                ratings.as_of_date = dt_raw.strftime('%Y-%m-%d')
    return instrument_rating


###############################################################################################
META_DATA = ('/home/hovhannes/Projects/Athena/test/test_recources/meta_data/'
             '13e37049-e3f3-11e7-a405-0003ff4cbff7.meta')
# INSTRUMENTRATING_DATA = '/home/hovhannes/Projects/Athena/test/test_recources/instrument_rating_data/' \
#                         'AEA002001013.pb'
INSTRUMENTRATING_LIST = populate_instrument_rating(META_DATA)
# irng = populate_history(INSTRUMENTRATING_DATA, META_DATA)
print(INSTRUMENTRATING_LIST)