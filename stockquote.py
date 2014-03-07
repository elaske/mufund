#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evan Laske
# @Date:   2014-03-01 23:12:45
# @Last Modified by:   Evan Laske
# @Last Modified time: 2014-03-07 01:43:37

import urllib
import re
import html5lib
from bs4 import BeautifulSoup

class StockQuote:
    """
    A class that handles scraping of a ticker symbol's data from Google Finance.
    """
    
    def __init__(self):
        self._url = 'http://finance.google.com/finance?q='
        self._ticker = ''

    def __init__(self, ticker):
        self._url = 'http://finance.google.com/finance?q='
        self._ticker = ticker
        # Grab the content since the requirements are here.
        self.update()

    def url():
        doc = "The URL that the quotes will be retrieved from."
        def fget(self):
            return self._url
        def fset(self, value):
            self._url = value
            # Grab the content from the new URL.
            self.update()
        def fdel(self):
            del self._url
        return locals()
    url = property(**url())

    def ticker():
        doc = "The ticker of the data to be collected."
        def fget(self):
            return self._data['tickerSymbol']
        def fset(self, value):
            self._ticker = value
            # Grab the content from the new ticker.
            self.update()
        def fdel(self):
            del self._ticker
        return locals()
    ticker = property(**ticker())

    def price():
        doc = "The price of the given ticker."
        def fget(self):
            return self._data['price']
        # No setter
        # No deleter 
        return locals()
    price = property(**price())

    def change():
        doc = "The change in price in absolute terms."
        def fget(self):
            return self._data['priceChange']
        # No setter
        # No deleter 
        return locals()
    change = property(**change())

    def percent():
        doc = "The percent change in price."
        def fget(self):
            return self._data['priceChangePercent']
        # No setter
        # No deleter 
        return locals()
    percent = property(**percent())

    def update(self):
        """
        Collect new data from the source URL and ticker.
        """
        # Grab the content from the new URL.
        self._content = urllib.urlopen(self._url + self._ticker).read()
        self._soup = BeautifulSoup(self._content)
        # temp_data = self._soup('div', id="sharebox-data")[0]
        # for meta in temp_data.contents:
        #     print meta, type(meta), meta.name
        # Get strip all of the meta tag attributes into a dictionary from the correct div tag container.
        self._data = {
            meta.get('itemprop'): meta.get('content') 
            for meta in self._soup('div', id="sharebox-data")[0].find_all('meta')
        }
        #print self._data
