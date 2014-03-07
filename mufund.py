#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: elaske
# @Date:   2014-03-01 21:45:31
# @Last Modified by:   Evan Laske
# @Last Modified time: 2014-03-07 01:44:18

import urllib
import urllib2
from bs4 import BeautifulSoup
import html5lib
import re
from stockquote import StockQuote

def main():
    ticker = "FBIOX"

    quoteURL = 'http://quotes.morningstar.com/fund/f?t='
    portfolioURL = 'http://portfolios.morningstar.com/fund/summary?t='
    holdingsURL = 'http://portfolios.morningstar.com/fund/holdings?t='
    googleFinanceURL = 'http://www.google.com/finance?q='

    # Test with a stock
    sq = StockQuote("goog")
    print sq.price, sq.change, sq.percent

    # Test with a mutual fund
    sq = StockQuote("fiuix")
    print sq.price, sq.change, sq.percent
    

# Standard main call
if __name__ == "__main__":
    main()