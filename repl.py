from pymongo import MongoClient
from runme import celery
from itertools import islice, chain
import json
import requests
import sys

with open('conf/settings.json') as json_data:
    args = json.load(json_data)

c = MongoClient(host=args['mongo_uri'],
                port=args['mongo_port'])
gm_db = c['glitch_mob']
gm_tix = gm_db['companies']
gm_fields = gm_db['fields']
gm_blob_data = gm_db['blobs']
gm_quarterly = gm_db['quarterly']
gm_annual = gm_db['annual']

