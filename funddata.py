#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evan Laske
# @Date:   2014-03-02 01:05:31
# @Last Modified by:   Evan Laske
# @Last Modified time: 2014-03-02 19:38:32

import urllib
import urllib2
import html5lib
from bs4 import BeautifulSoup
from stockquote import StockQuote
import json

class MutualFundData(StockQuote):
    """
    Gathers data from a given mutual fund. Comes from Google Finance & Morningstar.
    """
    quoteURL = 'http://quotes.morningstar.com/fund/f?t='
    portfolioURL = 'http://portfolios.morningstar.com/fund/summary?t='
    holdingsURL = 'http://portfolios.morningstar.com/fund/holdings?t='
    
    def __init__(self):
        super(MutualFundData, self).__init__()

    def __init__(self, ticker):
        super(MutualFundData, self).__init__(ticker)
        # Grab the content since the requirements are here.
        self.update()

    def update(self):
        """
        Updates the current set of data from the current URL / ticker settings.
        """
        # First, update the quote for the fund through StockQuote
        super(MutualFundData, self).update()

        # These URLs are from the Morningstar site scripts.
        ajaxURL = 'http://portfolios.morningstar.com/fund/ajax/'
        ajaxPage = 'holdings_tab?&t=XNAS:FBIOX&region=usa&culture=en-US&cur=USD&dataType=0&callback=?'
        # Grab the JSON data from the source
        jsonHoldings = urllib.urlopen(ajaxURL + ajaxPage).read()
        # Strip the leading and trailing characters so we can load it correctly.
        jsonHoldings = jsonHoldings.strip('?()')

        dictHoldings = json.loads(jsonHoldings)

        print dictHoldings.keys()

        # Create a soup for the HTML
        self._soup = BeautifulSoup(dictHoldings['htmlStr'])
        self._holding_data = self._soup('table', id='equity_holding_tab')
        self._price_data = self._soup('table', id='equityPrice_holding_tab')

        print self._holding_data
        print self._price_data

    def holdings(self):
        """
        Returns a tuple of {ticker : portfolio weight} for all available holdings.
        """