#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evan Laske
# @Date:   2014-03-01 21:45:31
# @Last Modified by:   Evan Laske
# @Last Modified time: 2015-03-16 17:15:11

import urllib
import urllib2
from bs4 import BeautifulSoup
import html5lib
import re
from stockquote import StockQuote
from funddata import MutualFundData
import logging
import argparse 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tickers', metavar='ticker', nargs='+', help='The ticker(s) of the funds to predict.')
    parser.add_argument('--logfile', dest='logfile', default='', help='Specify a log file to log info to.')
    parser.add_argument('--loglevel', dest='loglevel', default='', help='Specify a logging level to output.')
    args = parser.parse_args()

    # Logging configuration args
    logConfigArgs = dict()
    # If the log level was specified 
    if args.loglevel:
        # Convert it to something usable
        numeric_level = getattr(logging, args.loglevel.upper(), None)
        # Double-check it's a valid logging level
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.loglevel)
        logConfigArgs['level'] = numeric_level
    # If there was any of the logging files specified...
    if args.logfile:
        logConfigArgs['filename'] = args.logfile
        # This will make the log file be overwritten each time.
        logConfigArgs['filemode'] = 'w'

    # If any of the logging arguments are specified, configure logging
    if args.logfile or args.loglevel:
        logging.basicConfig(**logConfigArgs)

    # Gather the data from the given stocks
    testStockQuote(args.tickers)

    # Test the mutual fund data gathering
    testMutualFund(args.tickers)

def testStockQuote(tickers):
    """
    """
    for ticker in tickers:
        sq = StockQuote(ticker)
        print sq.ticker, sq.price, sq.change, sq.percent


def testMutualFund(tickers):
    """
    """
    for ticker in tickers:
        mfd = MutualFundData(ticker)
        print mfd.price, mfd.change, mfd.percent

        holdings = mfd.holdings()
        print holdings
        for h in holdings:
            print 'Retrieving {0} data...'.format(h)
            sq = StockQuote(h)
            delta = float(holdings[h])*float(sq.percent)/100
            holdings[h] = [holdings[h], sq.price, sq.change, sq.percent, delta]
            print delta, holdings[h], 'Complete.'
            print sq
        #print holdings
        print '\nESTIMATED CHANGE: {0}\nTOTAL COMPOSITION: {1}'.format(
            sum([v[4] for (k,v) in holdings.items()]),
            sum([float(v[0]) for (k,v) in holdings.items()]))

def randomTest():
    ticker = "FBIOX"

    quoteURL = 'http://quotes.morningstar.com/fund/f?t='
    portfolioURL = 'http://portfolios.morningstar.com/fund/summary?t='
    holdingsURL = 'http://portfolios.morningstar.com/fund/holdings?t='
    googleFinanceURL = 'http://www.google.com/finance?q='

    # Test with a stock
    #sq = StockQuote("goog")
    #print sq.price, sq.change, sq.percent
    #print sq

    # Test with a mutual fund
    sq = StockQuote("fiuix")
    print sq.price, sq.change, sq.percent
    mfd = MutualFundData("FBIOX")
    print mfd.price, mfd.change, mfd.percent

    holdings = mfd.holdings()
    #print holdings
    for h in holdings:
        print 'Retrieving {0} data...'.format(h)
        sq = StockQuote(h)
        delta = float(holdings[h])*float(sq.percent)/100
        holdings[h] = [holdings[h], sq.price, sq.change, sq.percent, delta]
        print 'Complete.'
    #print holdings
    print '\nESTIMATED CHANGE: {0}\nTOTAL COMPOSITION: {1}'.format(
        sum([v[4] for (k,v) in holdings.items()]),
        sum([float(v[0]) for (k,v) in holdings.items()]))

# Standard main call
if __name__ == "__main__":
    main()