#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evan Laske
# @Date:   2014-03-01 23:12:45
# @Last Modified by:   Evan Laske
# @Last Modified time: 2015-03-23 23:15:06

import urllib
import urllib2
import json
import logging
import copy

class StockQuoteEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StockQuote):
            tempDict = copy.deepcopy(obj.__dict__)

            # Remove all of the leading underscores
            for (k,v) in tempDict.items():
                if k[0] == '_':
                    tempDict[k[1:]] = v
                    del tempDict[k]
            # Let the base class throw the TypeError if there is one.
            return tempDict
        # Let the base class throw the TypeError that has occurred
        return json.JSONEncoder.default(self, obj)

class StockQuote(object):
    """
    A class that handles scraping of a ticker symbol's data from Google Finance.
    """
    default_data = {'c_fix': None, 'cp_fix': None, 'l_fix': None, 'e': None, 'lt': None, 'ltt': None}

    def __init__(self, ticker='', jsonString=''):
        if jsonString:
            self.fromJSON(jsonString=jsonString)
        else:
            self._url = 'http://finance.google.com/finance/info?q='
            self._ticker = ticker
            self._data = StockQuote.default_data
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

    @property
    def ticker(self):
        """The ticker of the data to be collected."""
        return self._ticker
    @ticker.setter
    def ticker(self, value):
        logging.debug('StockQuote ticker changed from {0} to {1}'.format(self._ticker, value))
        self._ticker = value
        # Grab the content from the new ticker.
        self.update()

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

            del self._content   # clean up, we don't need this anymore

        # Blanket catch so that any problems with urllib or loads() are caught
        except:
            # Set the data values back to default if there's an error.
            self._data = StockQuote.default_data

    def toJSON(self):
        # Human-readable
        return json.dumps(self, sort_keys=True, indent=4, separators=(',', ': '), cls=StockQuoteEncoder)

        # Single-line
        # return json.dumps(self, separators=(',',': '), cls=StockQuoteEncoder)
    
    def fromJSON(self, jsonString):
        tempDict = json.loads(jsonString)
        for a in tempDict.keys():
            setattr(self, '_' + a, tempDict[a])

if __name__ == '__main__':
    google = StockQuote('GOOGL')
    print google.toJSON()
    print StockQuote(jsonString=google.toJSON()).toJSON()
    if google.toJSON() == StockQuote(jsonString=google.toJSON()).toJSON():
        print "Success"
