#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: elaske
# @Date:   2014-03-01 21:45:31
# @Last Modified by:   Evan Laske
# @Last Modified time: 2014-03-02 00:22:36

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

    sq = StockQuote("goog")
    print sq.price, sq.change, sq.percent
    print sq

# Standard main call
if __name__ == "__main__":
    main()