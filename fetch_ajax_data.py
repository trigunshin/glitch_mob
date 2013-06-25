from pymongo import MongoClient
from runme import celery
from itertools import islice, chain
from tasks import process_request
import json
import requests

def chunk_fids(fid_array, chunk_size=10):
    fid_len = len(fid_array)
    cur = 0
    end = chunk_size
    ifids = iter(fid_array)
    ret = []

    while cur < fid_len:
        islice(ifids, chunk_size)
        ret.append(fid_array[cur:end])
        cur = end
        end = end + chunk_size
    return ret

def get_query_url(cid_seq, fid_seq, base_url):
    return base_url % (','.join([str(cid) for cid in cid_seq]),
                       ','.join([str(fid) for fid in fid_seq]))

def get_urls(companies, fid_groups, base_url):
    for cid in (company['cid'] for company in companies):
        for fid_group in fid_groups:
            yield get_query_url([cid], fid_group, base_url)

if __name__ == "__main__":
    with open('conf/settings.json') as json_data:
        args = json.load(json_data)

    c = MongoClient(host=args['mongo_uri'],
                    port=args['mongo_port'])
    gm_db = c['glitch_mob']
    gm_tix = gm_db['companies']
    gm_fields = gm_db['fields']

    companies = [company for company in gm_tix.find()]
    fids = [field['id'] for field in gm_fields.find()]
    FID_BATCH_SIZE = 10
    fid_groups = chunk_fids(fids, FID_BATCH_SIZE)

    for url in get_urls(companies, fid_groups, args['ajax_data_uri']):
        process_request.delay(url, args['mongo_uri'])