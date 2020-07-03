#!/usr/bin/env python3

import yfinance as yf
import test_display

tickers = ['MSFT', 'AAPL', 'ACB', 'GE', 'AAL',
    'DAL', 'BAC', 'SNAP', 'BA', 'UBER', 'TSLA',
    'GRPN', 'SBUX', 'T', 'AMZN', 'NFLX', 'NVDA', 'SPY',
    'BYND', 'BTC-USD']

#print(yf.Ticker('MSFT').info)

for ticker in tickers:
    # get stock info
    financial_data = yf.Ticker(ticker)
    
    # print stock info
    name = financial_data.info.get('shortName', financial_data.info.get('longName', ticker))
    openPrice = float(financial_data.info['regularMarketOpen'])
    price = float(financial_data.info['regularMarketPrice'])
    pct_change = 100 * (price - openPrice) / openPrice
    s = ticker + ': ' + price + ' - ' + pct_change
    test_display.scroll_word(0, 4, '       ' + s, 2)
