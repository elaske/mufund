#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evan Laske
# @Date:   2014-03-01 21:45:31
# @Last Modified by:   Evan Laske
# @Last Modified time: 2014-03-06 23:10:09

import urllib
import urllib2
from bs4 import BeautifulSoup
import html5lib
import re
from stockquote import StockQuote
from funddata import MutualFundData

def main():
    ticker = "FBIOX"

    quoteURL = 'http://quotes.morningstar.com/fund/f?t='
    portfolioURL = 'http://portfolios.morningstar.com/fund/summary?t='
    holdingsURL = 'http://portfolios.morningstar.com/fund/holdings?t='
    googleFinanceURL = 'http://www.google.com/finance?q='

    #sq = StockQuote("goog")
    #print sq.price, sq.change, sq.percent
    #print sq

    mfd = MutualFundData("FBIOX")
    print mfd.price, mfd.change, mfd.percent

    holdings = mfd.holdings()
    #print holdings
    for h in holdings:
        print 'Retrieving {0} data...'.format(h)
        sq = StockQuote(h)
        delta = float(holdings[h])*float(sq.percent)/100
        holdings[h] = [holdings[h], sq.price, sq.change, sq.percent, delta]
        print 'Complete.'
    #print holdings
    print '\nESTIMATED CHANGE: {0}\nTOTAL COMPOSITION: {1}'.format(
        sum([v[4] for (k,v) in holdings.items()]),
        sum([float(v[0]) for (k,v) in holdings.items()]))

# Standard main call
if __name__ == "__main__":
    main()