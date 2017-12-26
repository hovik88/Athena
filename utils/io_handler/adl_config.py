from __future__ import division, unicode_literals, print_function

from azure.datalake.store import core, lib, multithread


TENANT = '2b3b3aac-a5c3-4534-bc91-da1894967eb8'
RESOURCE = 'https://datalake.azure.net/'
CLIENT_ID = '44b532cd-a633-4af9-9357-6adb9fb35539'
CLIENT_SECRET = '2oxOuf68knjSIMHykLDKDWHu1t5uEH8P/F45Kt4IkTw='
STORE_NAME = 'scdmathenadev'
token = lib.auth(
    tenant_id=TENANT, client_secret=CLIENT_SECRET, client_id=CLIENT_ID, resource=RESOURCE)
