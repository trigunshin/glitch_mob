from pymongo import MongoClient
from runme import celery
from tasks import get_field_ids
from time import sleep
from bs4 import BeautifulSoup
import json
import requests

if __name__ == "__main__":
    with open('conf/settings.json') as json_data:
        args = json.load(json_data)

    c = MongoClient(host=args['mongo_uri'],
                    port=args['mongo_port'])
    gm_db = c['glitch_mob']
    gm_tickers = gm_db['companies']
    cid_cursor = gm_tickers.find()

    #cid=cid_cursor[0]['cid']
    #results = [get_cid.delay(args['base_uri'], ticker['symb'], regex, args['mongo_uri']) for ticker in ticker_cursor]

    fields_data = [{'group':'balance_sheet', 'url':args['balance_sheet_field_id_uri']},
                   {'group':'income_statement', 'url':args['income_statement_field_id_uri']},
                   {'group':'cash_flow', 'url':args['cash_flow_field_id_uri']}]
    for cid in cid_cursor[0:1]:
        for field in fields_data:
            print "working on fielddict:",str(field)
            get_field_ids.delay(field['url'],
                                cid['cid'],
                                field['group'],
                                args['mongo_uri'])

    #balance_url = args['balance_sheet_field_id_uri'] % cid

    """
    get_field_ids(args['balance_sheet_field_id_uri'],
                  cid,
                  'balance_sheet',
                  'kilrog.dyndns.org')
    #"""