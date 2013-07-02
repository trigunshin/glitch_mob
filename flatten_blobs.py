from pymongo import MongoClient
from runme import celery
from itertools import islice, chain
from tasks import insert_blob_data
import json
import requests
import sys

def getFieldDict(coll):
    ret={}
    all_fields = [field for field in coll.find()]
    for field in all_fields:
        ret[field['id']] = field
    return ret

def get_blob_fields(blob):
    blob_fields = []
    for field_id, field_data in blob['metrics'].items():
        field_data['id'] = str(field_id)
        blob_fields.append(field_data)
    return blob_fields

def get_blob_companies(blob):
    blob_companies = []
    for cid, cdata in blob['companies'].items():
        cdata['id'] = cid
        blob_companies.append(cdata)
    return blob_companies

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

# make dict of fields keyed by fid
field_dict = getFieldDict(gm_fields)

# make dict of companies keyed by cid or symb
companies = [company for company in gm_tix.find()]
cdict = {}
#cids = []
for cur in companies:
    #cids.append(cur['cid'])
    cdict[cur['cid']] = cur
    cdict[cur['symb']] = cur

#for blob in [b for b in gm_blob_data.find().limit(1)]:
all_blobs = [b for b in gm_blob_data.find()]
print "loaded all blobs to memory, processing tasks..."
for blob in all_blobs:
    # company or field failure means there weren't values
    try:
        blob_companies = get_blob_companies(blob)
        blob_fields = get_blob_fields(blob)
    except AttributeError, e:
        continue
    insert_blob_data(blob,
                           blob_companies,
                           blob_fields,
                           field_dict,
                           cdict,
                           args['mongo_uri'])

"""
for blob in [b for b in gm_blob_data.find()]:
    for cid in [cur_cmpny['id'] for cur_cmpny in get_blob_companies(blob)]:
        try:
            for field in get_blob_fields(blob):
                to_insert = {}
                to_insert.update(field)
                to_insert['category'] = field_dict[field['id']]['category']

                field_data = blob[cid][field['id']]['data']
                try:
                    # check year length to ignore a misc '1' field
                    for year in (year for year in field_data.iterkeys() if len(year) > 3):
                        for time, value in field_data[year].items():
                            if time == "year":  # annual data
                                ins = {'value':value, 'period':time, 'year':year, 'symb':cdict[cid]['symb']}
                                ins.update(to_insert)
                                gm_annual.insert(ins)
                            else:  #quarter data
                                ins = {'value':value, 'period':time, 'year':year, 'symb':cdict[cid]['symb']}
                                ins.update(to_insert)
                                gm_quarterly.insert(ins)
                except AttributeError, e:
                    # empty data fields are actually [], not {}...
                    print 'error:', e
                    print 'field_data:', field_data
                    continue
        except AttributeError,e:
            # empty metric fields are actually [], not {}...
            print 'error:', e
            print 'fields:', blob['metrics']
            continue
#"""
