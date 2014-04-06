#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evan Laske
# @Date:   2014-03-01 23:12:45
# @Last Modified by:   Evan Laske
# @Last Modified time: 2014-04-05 23:39:07

import urllib
import urllib2
import json
import logging

class StockQuote(object):
    """
    A class that handles scraping of a ticker symbol's data from Google Finance.
    """
    default_data = {'c_fix': None, 'cp_fix': None, 'l_fix': None, 'e': None, 'lt': None, 'ltt': None}
    
    def __init__(self):
        self._url = 'http://finance.google.com/finance/info?q='
        self._ticker = ''
        self._data = StockQuote.default_data

    def __init__(self, ticker):
        self._url = 'http://finance.google.com/finance/info?q='
        self._ticker = ticker
        logging.info('StockQuote created, ticker = {0}'.format(ticker))
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
        logging.debug('StockQuote ticker changed from {0} to {1}'.format(self._ticker, value))
        self._ticker = value
        # Grab the content from the new ticker.
        self.update()
    @ticker.deleter
    def ticker(self):
        del self._ticker

    @property
    def price(self):
        """The price of the given ticker."""
        return self._data['cp_fix']

    @property
    def change(self):
        """The change in price in absolute terms."""
        return self._data['c_fix']

    @property
    def percent(self):
        """The percent change in price."""
        return self._data['l_fix']

    @property
    def exchange(self):
        """The exchange that the given stock trades on."""
        return self._data['e']

    @property
    def last_trade(self):
        """The date & time at which the price was set."""
        return self._data['lt']

    @property
    def last_trade_time(self):
        """The time at which the price was set."""
        return self._data['ltt']

    def update(self):
        """
        Collect new data from the source URL and ticker.
        Defaults all values to 'None' if error.
        """
        logging.info('StockQuote.update()')

        # Catch the exception caused by Google giving crap data.
        try:
            # Grab the content from the new URL.
            lines = urllib.urlopen(self._url + self._ticker).read().splitlines()
            logging.debug('lines: {0}'.format(lines))

            # Format it into good JSON
            self._content = ''.join([x for x in lines if x not in ('// [', ']')])
            logging.debug('JSON: {0}'.format(self._content))

            self._data = json.loads(self._content)
            logging.debug('Data: {0}'.format(self._data))

        # Blanket catch so that any problems with urllib or loads() are caught
        except:
            # Set the data values back to default if there's an error.
            self._data = StockQuote.default_data
