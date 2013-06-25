from pymongo import MongoClient
from runme import celery
from itertools import islice, chain
import json
import requests

with open('conf/settings.json') as json_data:
    args = json.load(json_data)

c = MongoClient(host=args['mongo_uri'],
                port=args['mongo_port'])
gm_db = c['glitch_mob']
gm_tix = gm_db['companies']
gm_fields = gm_db['fields']
gm_data = gm_db['requests']
gm_blob_data = gm_db['blobs']

companies = [company for company in gm_tix.find()]
demo = companies[0]

cdict = {}
for cur in companies:
    cdict[cur['cid']] = cur
    cdict[cur['symb']] = cur
#"""
blob_tickers = set()
blob_data = set()
#all_requests = [r for r in gm_data.find()]
all_requests = [r for r in gm_data.find().limit(1)]
all_requests[0]['companies']


#for blob in [demo_data]:
for blob in all_requests:
    del blob['_id']
    # if we have a list, then skip it...
    if type(blob['companies']) is list:
        if len(blob['companies']) > 0:
            print "skipping multi-company data:", blob['companies']
        continue
    cid, comp_data = blob['companies'].items()[0]
    blob_tickers.add(comp_data['ticker'])
    blob_data.add(json.dumps(blob))
#blob_tickers

#new_blobs=[gm_blob_data.insert(json.loads(blob)) for blob in blob_data]
new_blobs=(json.loads(blob) for blob in blob_data)
#[gm_blob_data.insert(json.loads(blob)) for blob in blob_data]

#gm_blob_data.insert(new_blobs)

#for cur_blob in gm_data.iter:
#"""

