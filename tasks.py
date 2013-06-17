from runme import celery
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
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

    soup = BeautifulSoup(requests.get(base_url % cid).text)
    for tr in soup.find_all('tr', class_='metric'):
        f_id = tr['id'].split('-')[0]
        f_name = tr.find_all('a')[0].text
        print "fuckmerotten"
        coll.update({'id':f_id},
                    {'id':f_id, 'name':f_name, 'category':field_group},
                    upsert=True)
    return (True, base_url % cid)