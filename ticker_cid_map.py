from pymongo import MongoClient
from runme import celery
from tasks import get_cid
#from bs4 import BeautifulSoup
import re
import json
import requests

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
    cid = get_cid.delay(args['base_uri'], ticker, regex, args['mongo_uri'])
    print cid
    print cid.ready()
    print cid.get(timeout=4)

    #print args['base_uri'] % ticker, cid
    #top = trade_hist.find({'price_currency':cur,'item':item}).sort('tid',-1).limit(1)
