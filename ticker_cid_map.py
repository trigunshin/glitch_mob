from pymongo import MongoClient
from runme import celery
from bs4 import BeautifulSoup
import re
import json
import requests

@celery.task
def get_cid(base_url,
            ticker,
            regex,
            db_url,
            db_port=27017,
            db_name='glitch_mob',
            coll_name='companies',
            regex_result_field='cid'):

    c = MongoClient(host=db_url,
                    port=db_port)
    gm_db = c[db_name]
    gm_tickers = gm_db[coll_name]

    request_result = requests.get(base_url % ticker)
    regex_result = regex.search(request_result.text)

    if regex_result:
        cid = regex_result.group(regex_result_field)
        gm_tickers.insert({'symb':ticker, 'cid':cid})

        return (ticker, cid)
    else:
        return None

if __name__ == "__main__":
    with open('conf/settings.json') as json_data:
        args = json.load(json_data)

    c = MongoClient(host=args['mongo_uri'],
                    port=args['mongo_port'])
    v_db = c['vortex']
    #gm_db = c['glitch_mob']

    vortex_tickers = v_db['tickers']
    #gm_tickers = gm_db['companies']
    #tickerCursor = vortex_tickers.find()

    regex = re.compile("companyid'?='?(?P<cid>[\d]+)")

    ticker='aiz'
    cid = get_cid(args['base_uri'], ticker, regex, args['mongo_uri'])
    print args['base_uri'] % ticker, cid
    #top = trade_hist.find({'price_currency':cur,'item':item}).sort('tid',-1).limit(1)
