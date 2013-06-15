from pymongo import MongoClient
from runme import celery
from tasks import get_cid
from time import sleep
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
    vortex_tickers = v_db['tickers']
    #gm_db = c['glitch_mob']
    #gm_tickers = gm_db['companies']
    ticker_cursor = vortex_tickers.find()
    #
    regex = re.compile("ticker='[\w]+:(?P<ticker>[\w]+)' companyid'?='?(?P<cid>[\d]+)")

    #ticker='aiz'
    #tlist=
    #print "running over tickers:",ticker_cursor[0:4]
    #results = [get_cid.delay(args['base_uri'], ticker['symb'], regex, args['mongo_uri']) for ticker in ticker_cursor[0:5]]
    results = [get_cid.delay(args['base_uri'], ticker['symb'], regex, args['mongo_uri']) for ticker in ticker_cursor]

    while len([result for result in results if not result.ready()]) > 0:
        print "results not done yet, sleeping..."
        sleep(2)



    #cid = get_cid.delay(args['base_uri'], ticker, regex, args['mongo_uri'])
    #print cid
    #print cid.ready()
    #print cid.get(timeout=4)

    #print args['base_uri'] % ticker, cid

    #top = trade_hist.find({'price_currency':cur,'item':item}).sort('tid',-1).limit(1)
