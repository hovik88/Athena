from __future__ import division, print_function, unicode_literals

from pyspark import SparkConf, SparkContext


conf = SparkConf().setAppName('Rating_data_processor')
sc = SparkContext(conf=conf)
sc._jsc.hadoopConfiguration().set("fs.adl.impl", "org.apache.hadoop.fs.adl.AdlFileSystem")
sc._jsc.hadoopConfiguration().set("fs.AbstractFileSystem.adl.impl", "org.apache.hadoop.fs.adl.Adl")
sc._jsc.hadoopConfiguration().set("dfs.adls.oauth2.access.token.provider.type", "ClientCredential")
sc._jsc.hadoopConfiguration().set(
    "dfs.adls.oauth2.access.token.provider",
    "org.apache.hadoop.fs.adls.oauth2.ConfCredentialBasedAccessTokenProvider")
sc._jsc.hadoopConfiguration().set(
    "dfs.adls.oauth2.client.id", "44b532cd-a633-4af9-9357-6adb9fb35539")
sc._jsc.hadoopConfiguration().set(
    "dfs.adls.oauth2.credential", "2oxOuf68knjSIMHykLDKDWHu1t5uEH8P/F45Kt4IkTw=")
sc._jsc.hadoopConfiguration().set(
    "dfs.adls.oauth2.refresh.url",
    "https://login.microsoftonline.com/2b3b3aac-a5c3-4534-bc91-da1894967eb8/oauth2/token")
