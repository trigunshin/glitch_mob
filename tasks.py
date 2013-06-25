from runme import celery
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import json
from time import sleep

@celery.task
def add(x, y):
    return x + y

@celery.task
def get_cid(base_url,
            ticker,
            cid_regex,
            db_url,
            db_port=27017,
            db_name='glitch_mob',
            coll_name='companies',
            regex_result_field='cid'):

    c = MongoClient(host=db_url,
                    port=db_port)
    gm_db = c[db_name]
    gm_tickers = gm_db[coll_name]
    print "working on", ticker
    request_result = requests.get(base_url % ticker)
    regex_result = cid_regex.search(request_result.text)

    sleep(1)

    if regex_result:
        match_ticker = regex_result.group('ticker')
        print 'm_t:',match_ticker,'\tt:',ticker
        if match_ticker == ticker:
            cid = regex_result.group(regex_result_field)
            gm_tickers.insert({'symb':ticker, 'cid':cid})

            return (ticker, cid)
        else:
            return None
    else:
        return None

@celery.task
def get_field_ids(base_url,
                  cid,
                  field_group,
                  db_url,
                  db_port=27017,
                  db_name='glitch_mob',
                  coll_name='fields'):
    c = MongoClient(host=db_url,
                    port=db_port)
    gm_db = c[db_name]
    coll = gm_db[coll_name]
    print "working on", cid
    sleep(1)
    soup = BeautifulSoup(requests.get(base_url % cid).text)
    for tr in soup.find_all('tr', class_='metric'):
        f_id = tr['id'].split('-')[0]
        f_name = tr.find_all('a')[0].text
        coll.update({'id':f_id},
                    {'id':f_id, 'name':f_name, 'category':field_group},
                    upsert=True)
    return (True, base_url % cid)

@celery.task
def process_request(url,
                     db_url,
                     db_port=27017,
                     db_name='glitch_mob',
                     coll_name='requests'):
    c = MongoClient(host=db_url,
                    port=db_port)
    gm_db = c[db_name]
    coll = gm_db[coll_name]
    print "working on", url
    sleep(1)
    jtext = requests.get(url).text
    coll.insert(json.loads(jtext))
    return (True, url, json)

@celery.task
def insert_blob_data(blob,
                     blob_companies,
                     blob_fields,
                     field_category_map,
                     cid_symb_map,

                     db_url,
                     db_port=27017,
                     db_name='glitch_mob',
                     annual_coll_name='annual',
                     quarterly_coll_name='quarterly'):
    c = MongoClient(host=db_url,
                    port=db_port)
    gm_db = c[db_name]
    annual_coll = gm_db[annual_coll_name]
    quarterly_coll = gm_db[quarterly_coll_name]

    for cid in [cur['id'] for cur in blob_companies]:
        try:
            for field in blob_fields:
                to_insert = {}
                to_insert.update(field)
                to_insert['category'] = field_category_map[field['id']]['category']

                field_data = blob[cid][field['id']]['data']
                try:
                    # check year length to ignore a misc '1' field
                    for year in (year for year in field_data.iterkeys() if len(year) > 3):
                        for time, value in field_data[year].items():
                            if time == "year":  # annual data
                                ins = {'value':value, 'period':time, 'year':year, 'symb':cid_symb_map[cid]['symb']}
                                ins.update(to_insert)
                                annual_coll.insert(ins)
                            else:  #quarter data
                                ins = {'value':value, 'period':time, 'year':year, 'symb':cid_symb_map[cid]['symb']}
                                ins.update(to_insert)
                                quarterly_coll.insert(ins)
                except AttributeError, e:
                    # empty data fields are actually [], not {}...
                    #print 'error:', e
                    #print 'field_data:', field_data
                    continue
        except AttributeError,e:
            # empty metric fields are actually [], not {}...
            #print 'error:', e
            #print 'fields:', blob['metrics']
            continue