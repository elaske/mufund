#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evan Laske
# @Date:   2014-03-01 23:12:45
# @Last Modified by:   Evan Laske
# @Last Modified time: 2014-03-07 21:35:20

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

    @property
    def url(self):
        """The URL that the quotes will be retrieved from."""
        return self._url
    @url.setter
    def url(self, value):
        self._url = value
        # Grab the content from the new URL.
        self.update()
    @url.deleter
    def url(self):
        del self._url

    @property
    def ticker(self):
        """The ticker of the data to be collected."""
        return self._data['tickerSymbol']
    @ticker.setter
    def ticker(self, value):
        self._ticker = value
        # Grab the content from the new ticker.
        self.update()
    @ticker.deleter
    def ticker(self):
        del self._ticker

    @property
    def price(self):
        """The price of the given ticker."""
        return self._data['price']

    @property
    def change(self):
        """The change in price in absolute terms."""
        return self._data['priceChange']

    @property
    def percent(self):
        """The percent change in price."""
        return self._data['priceChangePercent']

    def update(self):
        """
        Collect new data from the source URL and ticker.
        """
        # Grab the content from the new URL.
        self._content = urllib.urlopen(self._url + self._ticker).read()
        self._soup = BeautifulSoup(self._content)
        # Get strip all of the meta tag attributes into a dictionary from the correct div tag container.
        self._data = {
            meta.get('itemprop'): meta.get('content') 
            for meta in self._soup('div', id="sharebox-data")[0].find_all('meta')
        }
