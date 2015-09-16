#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evan Laske
# @Date:   2015-03-16 17:24:58
# @Last Modified by:   Evan Laske
# @Last Modified time: 2015-03-23 23:08:09

import datetime
import json
import logging
import copy
from StockQuote import StockQuote, StockQuoteEncoder

class StockTransactionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StockTransaction):
            tempDict = copy.deepcopy(obj.__dict__)
            # Remove all of the leading underscores
            for (k,v) in tempDict.items():
                if k[0] == '_':
                    tempDict[k[1:]] = v
                    del tempDict[k]
            if 'quote' in tempDict.keys() and tempDict['quote']:
                tempDict['quote'] = StockQuoteEncoder().default(tempDict['quote'])
            return tempDict
        # Let the base class throw the TypeError that has occurred
        return json.JSONEncoder.default(self, obj)

class StockTransaction(object):
    """
    A class that defines a stock transaction.
    """

    def __init__(self, 
                date=None,
                time=None,
                ticker='',
                price=0.0,
                quote=None,
                shares=0.0,
                amount=0.0,
                ttype='',
                jsonString=''
            ):
        if jsonString:
            self.fromJSON(jsonString=jsonString)
        else:
            self.date = date
            self.time = time
            if ticker:
                self.quote = StockQuote(ticker)
            else:
                self.quote = quote
            self.price = price
            self.shares = shares
            self.amount = amount
            self.ttype = ttype

    @property
    def date(self):
        "The date the transaction was executed."
        return self._date
    @date.setter
    def date(self, value):
        self._date = value
    @date.deleter
    def date(self):
        del self._date

    @property
    def time(self):
        "The time this transaction was executed (optional)."
        return self._time
    @time.setter
    def time(self, value):
        self._time = value
    @time.deleter
    def time(self):
        del self._time

    @property
    def ticker(self):
        "The ticker of the security."
        if self._quote:
            return self._quote.ticker
        else:
            return ''
    @ticker.setter
    def ticker(self, value):
        self._quote = StockQuote(ticker)

    @property
    def price(self):
        "The price of the security."
        return self._price
    @price.setter
    def price(self, value):
        self._price = value
    @price.deleter
    def price(self):
        del self._price

    @property
    def quote(self):
        "The stock quote associated with this transaction."
        return self._quote
    @quote.setter
    def quote(self, value):
        self._quote = value
    @quote.deleter
    def quote(self):
        del self._quote

    @property
    def shares(self):
        "The number of shares traded in this transaction."
        return self._shares
    @shares.setter
    def shares(self, value):
        self._shares = value
    @shares.deleter
    def shares(self):
        del self._shares

    @property
    def amount(self):
        "The amount of the transaction."
        return self._amount
    @amount.setter
    def amount(self, value):
        self._amount = value
    @amount.deleter
    def amount(self):
        del self._amount

    @property
    def ttype(self):
        "The transaction type."
        return self._ttype
    @ttype.setter
    def ttype(self, value):
        self._ttype = value
    @ttype.deleter
    def ttype(self):
        del self._ttype

    def toJSON(self):
        # Human-readable
        return json.dumps(self, sort_keys=True, indent=4, separators=(',', ': '), cls=StockTransactionEncoder)

        # Single-line
        # return json.dumps(self, separators=(',',': '), cls=StockTransactionEncoder)

    def fromJSON(self, jsonString):
        tempDict = json.loads(jsonString)
        for a in tempDict.keys():
            # recursively convert stock quote
            if a == 'quote':
                setattr(self, '_' + a, StockQuote(jsonString=json.dumps(tempDict[a])))
            else:
                setattr(self, '_' + a, tempDict[a])

if __name__ == '__main__':
    # print StockQuote('')
    st = StockTransaction(ticker='GOOGL')
    print st.toJSON()
    print StockTransaction(jsonString=st.toJSON()).toJSON()
    if st.toJSON() == StockTransaction(jsonString=st.toJSON()).toJSON():
        print "Success"
