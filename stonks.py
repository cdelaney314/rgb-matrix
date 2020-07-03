#!/usr/bin/env python3
import requests
import re
import json
import matrixlib
#from bs4 import BeautifulSoup

tickers = ['MSFT', 'AAPL', 'ACB', 'GE', 'AAL',
    'DAL', 'BAC', 'SNAP', 'BA', 'UBER', 'TSLA',
    'GRPN', 'SBUX', 'T', 'AMZN', 'NFLX', 'NVDA', 'SPY',
    'BYND', 'BTC-USD']

def stonks_handler(symbol):
    '''gives you stock info by scraping yahoo finance'''

    url = 'https://finance.yahoo.com/quote/'

    if symbol:
        url += symbol
    else:
        return '!stonks <symbol>'
    response  = requests.get(url)
    if url != response.url:
        return 'Could not get ' + symbol + ' price' 
    stock_html = response.text
    price = re.search(r'regularMarketPrice.*?({.*?})', stock_html)
    change = re.search(r'regularMarketChangePercent.*?({.*?})', stock_html)
    if price:
        price = json.loads(price.group(1))['raw']
        change = json.loads(change.group(1))['raw']
        reply = '$' + str(price) + (' ' if change < 0 else ' +') + '{:.2f}'.format(change) + '%'
        if change < 0:
            return reply
        return reply
    return 'Could not get ' + symbol + ' price'

while True:
    for symbol in tickers:
        out = symbol + ': ' + stonks_handler(symbol)
        print(out)
        color = (matrixlib.pure_green if '+' in out else matrixlib.pure_red)
        matrixlib.scroll_text(0, 4, '     ' + out, color)
