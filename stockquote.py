#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evan Laske
# @Date:   2014-03-01 23:12:45
# @Last Modified by:   Evan Laske
# @Last Modified time: 2014-03-02 00:30:55

import urllib
import re

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
            return self._ticker
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
            m = re.search('id="ref_[0-9]*_l".*?>(.*?)<', self._content)
            if m:
                price = m.group(1)
            else:
                price = 'No quote available for symbol'
            return price
        # No setter
        # No deleter 
        return locals()
    price = property(**price())

    def change():
        doc = "The change in price in absolute terms."
        def fget(self):
            m = re.search('id="ref_[0-9]*_c".*?>(.*?)<', self._content)
            if m:
                change = m.group(1)
            else:
                change = 'No quote available for symbol'
            return change
        # No setter
        # No deleter 
        return locals()
    change = property(**change())

    def percent():
        doc = "The percent change in price."
        def fget(self):
            m = re.search('id="ref_[0-9]*_cp".*?>(.*?)<', self._content)
            if m:
                percent = m.group(1).strip('()%')
            else:
                percent = 'No quote available for symbol'
            return percent
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

