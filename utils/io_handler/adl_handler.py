from __future__ import division, unicode_literals, print_function
from spark_config.adl_spark_config import sc
from utils.io_handler import adl_config
from azure.datalake.store import core, lib, multithread

def adl_download(url_path):
    data = sc.textFile(url_path)
    return data


def adl_uplaod():
    pass
adl = core.AzureDLFileSystem(adl_config.token, store_name=adl_config.STORE_NAME)
# print(adl.ls('rating/'))
# data = adl_download("adl://scdmathenadev.azuredatalakestore.net/raw/13e37049-e3f3-11e7-a405-0003ff4cbff7.raw")
# print(data.collect())
# data.coalesce(1).save('adl://scdmathenadev.azuredatalakestore.net/rating/AEA0002010112.pb')
# a = '/home/hovhannes/Projects/Athena/test/test_recources/instrument_rating_data/AEA000201011.pb'
#
# path = 'adl://scdmathenadev.azuredatalakestore.net/rating/AEA0002010112.pb'
# rdd = sc.textFile(a)
#
# rdd.coalesce(1).saveAsTextFile(path)
