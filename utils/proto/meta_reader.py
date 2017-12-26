from __future__ import print_function, division, unicode_literals

from utils.io_handler.proto_io import meta_data_reader
from utils.io_handler.adl_handler import adl_download
from spark_config.adl_spark_config import sc


from utils.io_handler.file_reader import raw_data_reader

def meta_data_parser(data):
    data = meta_data_reader(data)
    raw_data = data.raw_data
    if raw_data:
        rows = [i for i in raw_data.split('\n')[1:] if i]  # 'AEA000201011,2017-05-30,(P)A1'
        print(rows)
        rows = sc.parallelize(rows)
    else:
        rows = adl_download(data.raw_data_url)
        header = rows.take(1)
        rows = rows.filter(lambda row: row != header)
    rdd = rows.map(lambda x: x.split(','))  # ['AEA000201011', '2017-05-30', '(P)A1']
    grouping = rdd.groupBy(lambda x: x[0])  # ('AEA000201011', ['AEA000201011', '2017-05-30', '(P)A1'])
    ids_dict_list = []
    for isin, group in grouping:
        if len(group.data) > 1:
            date_ = []
            rating = []
            id = group.data[0][0]
            for data_ in group.data:
                date_.append(data_[1])
                rating.append(data_[2])
            ids_dict_list.append(dict(id=id, as_of_date=date_, rating=rating))
        elif len(group.data) == 1:
            group_data = group.data[0]
            id  = group_data[0]
            date_ = [group_data[1]]
            rating = [group_data[2]]
            ids_dict_list.append(dict(id=id, as_of_date=date_, rating=rating))

    metadata = data.request.headers['metadata']
    api_asofdate = metadata.split('"api_asofdate"  : "')[-1].split('T')[0]
    source = metadata.split('"api_source" : "')[-1].split('"')[0]
    # rdd2 = sc.parallelize(ids_dict_list)
    data_list = []
    if source == 'Moodys':
        for data_dict in ids_dict_list:
            md_id_data = dict.fromkeys(['Identifier', 'mdy_latest_rating', 'source'])
            as_of_date = data_dict['as_of_date']
            if not as_of_date:
                as_of_date = api_asofdate
            if len(data_dict['rating']) > 1:
                moodys_rating = []
                for rating_ in data_dict['rating']:
                    rating_ = '{}_MDY_RATING_CLASS'.format(rating_.split('(P)')[-1])
                    moodys_rating.append(rating_)
            else:
                moodys_rating = ['{}_MDY_RATING_CLASS'.format(
                    data_dict['rating'][0].split('(P)')[-1])]
            md_id_data['Identifier'] = dict(id=data_dict['id'], id_type='ISIN')
            md_id_data['mdy_latest_rating'] = dict(rating=moodys_rating, as_of_date=as_of_date)
            md_id_data['source'] = source
            data_list.append(md_id_data)
    elif source == 'SnP':
        for data_dict in ids_dict_list:
            snp_id_data = dict.fromkeys(['Identifier', 'snp_latest_rating', 'source'])
            as_of_date = data_dict['as_of_date']
            if not as_of_date:
                as_of_date = api_asofdate
            if len(data_dict['rating']) > 1:
                snp_rating = []
                for rating_ in data_dict['rating']:
                    rating_ = '{}_SNP_RATING_CLASS'.format(
                        rating_.split('(P)')[-1].replace('+', 'ppp').replace('-', 'mmm'))
                    snp_rating.append(rating_)
            else:
                snp_rating = ['{}_SNP_RATING_CLASS'.format(
                    data_dict['rating'].split('(P)')[-1].replace('+', 'ppp').replace('-', 'mmm'))]
            snp_id_data['Identifier'] = dict(id=data_dict['id'], id_type='ISIN')
            snp_id_data['snp_latest_rating'] = dict(rating=snp_rating, as_of_date=as_of_date)
            snp_id_data['source'] = source
            data_list.append(snp_id_data)
    elif source == 'Fitch':
        for data_dict in ids_dict_list:
            fitch_id_data = dict.fromkeys(['Identifier', 'fitch_latest_rating', 'source'])
            as_of_date = data_dict['as_of_date']
            if not as_of_date:
                as_of_date = api_asofdate
            if len(data_dict['rating']) > 1:
                fitch_rating = []
                for rating_ in data_dict['rating']:
                    rating_ = '{}_FITCH_RATING_CLASS'.format(
                        rating_.split('(P)')[-1].replace('+', 'ppp').replace('-', 'mmm'))
                    fitch_rating.append(rating_)
            else:
                fitch_rating = ['{}_FITCH_RATING_CLASS'.format(
                    data_dict['rating'].split('(P)')[-1].replace('+', 'ppp').replace('-', 'mmm'))]
            fitch_id_data['Identifier'] = dict(id=data_dict['id'], id_type='ISIN')
            fitch_id_data['fitch_latest_rating'] = dict(rating=fitch_rating, as_of_date=as_of_date)
            fitch_id_data['source'] = source
            data_list.append(fitch_id_data)
    return data_list







# aaa = meta_data_reader('/home/hovhannes/Projects/Athena/test/test_recources/meta_data/13e37049-e3f3-11e7-a405-0003ff4cbff7.meta')
# input_data_parser('/home/hovhannes/Projects/Athena/test/test_recources/meta_data/13e37049-e3f3-11e7-a405-0003ff4cbff7.meta')
data_list = meta_data_parser('/home/hovhannes/Projects/Athena/test/test_recources/meta_data/13e37049-e3f3-11e7-a405-0003ff4cbff7.meta')
print(data_list)