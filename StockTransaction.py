#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evan Laske
# @Date:   2015-03-16 17:24:58
# @Last Modified by:   Evan Laske
# @Last Modified time: 2015-03-17 00:13:28

import datetime
import json
import logging
from StockQuote import StockQuote, StockQuoteEncoder

class StockTransactionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StockTransaction):
            tempDict = obj.__dict__
            # Remove all of the leading underscores
            for (k,v) in tempDict.items():
                if k[0] == '_':
                    tempDict[k[1:]] = v
                    del tempDict[k]
            tempDict['quote'] = StockQuoteEncoder().default(tempDict['quote'])
            return tempDict
        # Let the base class throw the TypeError that has occurred
        return json.JSONEncoder.default(self, obj)

class StockTransactionDecoder(json.JSONDecoder):
    def default(self, obj):
        #return json.JSONDecoder.default(self, obj.__dict__)
        pass

class StockTransaction(object):
    """
    A class that defines a stock transaction.
    """

    def __init__(self, ttype=None):
        self._date = ''
        self._time = ''
        print self._time
        self._ticker = ''
        self._price = 0.0
        self._quote = StockQuote()
        self._shares = 0.0
        self._amount = 0.0

        if ttype:
            self._ttype = ttype
        else: 
            self._ttype = ''

    @property
    def date(self):
        "The date the transaction was executed."
        return self._date
    @date.setter
    def date(self, value):
        self._date = value
    @date.getter
    def date(self):
        del self._date

    @property
    def time(self):
        "The time this transaction was executed (optional)."
        return self._time
    @time.setter
    def time(self, value):
        self._time = value
    @time.getter
    def time(self):
        del self._time

    @property
    def ticker(self):
        "The ticker of the security."
        return self._ticker
    @ticker.setter
    def ticker(self, value):
        self._ticker = str(value)
    @ticker.getter
    def ticker(self):
        del self._ticker

    @property
    def price(self):
        "The price of the security."
        return self._price
    @price.setter
    def price(self, value):
        self._price = value
    @price.getter
    def price(self):
        del self._price

    @property
    def quote(self):
        "The stock quote associated with this transaction."
        return self._quote
    @quote.setter
    def quote(self, value):
        self._quote = value
    @quote.getter
    def quote(self):
        del self._quote

    @property
    def shares(self):
        "The number of shares traded in this transaction."
        return self._shares
    @shares.setter
    def shares(self, value):
        self._shares = value
    @shares.getter
    def shares(self):
        del self._shares

    @property
    def amount(self):
        "The amount of the transaction."
        return self._amount
    @amount.setter
    def amount(self, value):
        self._amount = value
    @amount.getter
    def amount(self):
        del self._amount

    @property
    def ttype(self):
        "The transaction type."
        return self._ttype
    @ttype.setter
    def ttype(self, value):
        self._ttype = value
    @ttype.getter
    def ttype(self):
        del self._ttype

    def __str__(self):
        # Human-readable
        return json.dumps(self, sort_keys=True, indent=4, separators=(',', ': '), cls=StockTransactionEncoder)

        # Single-line
        # return json.dumps(self, separators=(',',': '), cls=StockTransactionEncoder)

if __name__ == '__main__':
    print StockQuote('')
    print StockTransaction('Buy')
