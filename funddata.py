#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evan Laske
# @Date:   2014-03-02 01:05:31
# @Last Modified by:   Evan Laske
# @Last Modified time: 2014-03-09 23:20:05

import urllib
import urllib2
import html5lib
from bs4 import BeautifulSoup
from bs4 import element
from stockquote import StockQuote
import json
from collections import OrderedDict
import logging

class MutualFundData(StockQuote):
    """
    Gathers data from a given mutual fund. Comes from Google Finance & Morningstar.
    """
    quoteURL = 'http://quotes.morningstar.com/fund/f?t='
    portfolioURL = 'http://portfolios.morningstar.com/fund/summary?t='
    holdingsURL = 'http://portfolios.morningstar.com/fund/holdings?t='
    
    def __init__(self):
        self._url = 'http://finance.google.com/finance?q='
        self._ticker = ''
        logging.info('MutualFundData created, no ticker')

    def __init__(self, ticker):
        self._url = 'http://finance.google.com/finance?q='
        self._ticker = ticker
        logging.info('MutualFundData created, ticker = {0}'.format(ticker))
        # Grab the content since the requirements are here.
        self.update()

    def update(self):
        """
        Updates the current set of data from the current URL / ticker settings.
        """
        # First, update the quote for the fund through StockQuote
        super(MutualFundData, self).update()
        logging.info('MutualFundData.update()')

        # These URLs are from the Morningstar site scripts.
        ajaxURL = 'http://portfolios.morningstar.com/fund/ajax/'
        ajaxPage = 'holdings_tab?&t=XNAS:FBIOX&region=usa&culture=en-US&cur=USD&dataType=0&callback=?'
        # Grab the JSON data from the source
        jsonHoldings = urllib.urlopen(ajaxURL + ajaxPage).read()
        # Strip the leading and trailing characters so we can load it correctly.
        jsonHoldings = jsonHoldings.strip('?()')
        dictHoldings = json.loads(jsonHoldings)
        logging.debug('JSON Dict Keys: {0}'.format(dictHoldings.keys()))

        # Create a soup for the HTML
        self._soup = BeautifulSoup(dictHoldings['htmlStr'])
        self._holding_data = self._soup('table', id='equity_holding_tab')
        logging.debug('Holding Tab: {0}'.format(self._holding_data))
        self._price_data = self._soup('table', id='equityPrice_holding_tab')
        logging.debug('Price Tab: {0}'.format(self._price_data))

    def holdings(self):
        """
        Returns a tuple of {ticker : portfolio weight} for all available holdings.
        """
        logging.info('MutualFundData.holdings()')

        # -------------------- HOLDING DATA TABLE --------------------

        # Within the only <table> and within the only <thead>, get all of the header cells.
        holdingHeaderTags = self._holding_data[0]('thead')[0]('th')
        # Remove all of the extranneous sub-tags - we only care about strings.
        holdingHeaderList = [filter(lambda x: isinstance(x, element.NavigableString), e.contents) for e in holdingHeaderTags]
        # Convert the NavigableStrings into actual strings
        holdingHeaderStrings = [[str(i) for i in l] for l in holdingHeaderList]
        # Join the sub-list strings with spaces to get a list of combined strings
        holdingHeaderStrings = [' '.join(i) for i in holdingHeaderStrings]

        logging.debug('Holding Header List: {0}'.format(holdingHeaderList))
        logging.debug('Holding Header Strings: {0}'.format(holdingHeaderStrings))

        # Remove all the extra whitespace from any of these strings.
        holdingHeaderStrings = [' '.join(s.split()) for s in holdingHeaderStrings]
        logging.debug('Combined Holding Header Strings: {0}'.format(holdingHeaderStrings))

        # This grabs the correct <tbody> tag which holds the table data
        tbody = self._holding_data[0]('tbody', id='holding_epage0')
        # There are "empty" rows, but they have a class specified.
        # The data rows are undecorated <tr>, so only take those:
        holdingRows = tbody[0]('tr', class_='')

        logging.debug('Holding Data Rows: {0}'.format(holdingRows))
        logging.debug('Example Row Content ([0].contents): {0}'.format(holdingRows[0].contents))

        # Remove all of the non-tags to remove extranneous objects.
        holdingRowList = [filter(lambda x: isinstance(x, element.Tag), e.contents) for e in holdingRows]
        logging.debug('Example Filtered Rows: {0}'.format(holdingRowList[0]))
        # Remove the extra <td> that doesn't match up with the <th> header elements
        for r in holdingRowList:
            del r[3]
        logging.debug('Example Trimmed Rows: {0}'.format(holdingRowList[0]))

        # For each row's elements, get the only string from it. 
        # If there so happens to be more than one, it will combine them.
        holdingRowStrings = [[' '.join([s for s in e.strings]) for e in row] for row in holdingRowList]
        logging.debug('Row Strings: {0}'.format(holdingRowStrings))

        # Put the holding data into a dictionary
        holdingData = OrderedDict()
        # Using an OrderedDict to keep the sorting order from the website.
        for row in holdingRowStrings:
            temp = OrderedDict()
            # Manually change the holding data header. 
            # Makes more sense than "Top 25 Holdings" when accessed later.
            temp["Holding"] = row[1]
            # Ignore the first 3 items
            for index in range(3, len(row)):
                # Only add data where the header actually means something.
                if holdingHeaderStrings[index]:
                    # Map the header strings as keys and the row data as the data.
                    temp[holdingHeaderStrings[index]] = row[index]
            # Use the name of the holding as the key for this whole thing.
            holdingData[row[1]] = temp

        logging.debug('New Data Dict: {0}'.format(holdingData))

        # --------------------- PRICE DATA TABLE ---------------------

        # This grabs the correct <tbody> tag which holds the table data
        tbody = self._price_data[0]('tbody', id='holding_price_page0')
        # There are "empty" rows, but they have a class specified.
        # The data rows are undecorated <tr>, so only take those:
        holdingRows = tbody[0]('tr', class_='')
        # Remove all of the non-tags to remove extranneous objects.
        holdingRowList = [filter(lambda x: isinstance(x, element.Tag), e.contents) for e in holdingRows]
        # print "\nPrice Row:"
        # print holdingRowList[0], len(holdingRowList[0])

        # print '\nStrings:'
        # For each row's elements, get the only string from it. 
        # If there so happens to be more than one, it will combine them.
        holdingRowStrings = [[' '.join([s for s in e.strings]) for e in row] for row in holdingRowList]
        # Remove extra whitespace from the data.
        holdingRowStrings = [[' '.join(s.split()) for s in l] for l in holdingRowStrings]
        # Filter out empty strings - they're falsy
        holdingRowStrings = [filter(lambda x: x, e) for e in holdingRowStrings]
        # print holdingRowStrings

        # Within the only <table> and within the only <thead>, get all of the header cells.
        holdingHeaderTags = self._price_data[0]('thead')[0]('th')
        # Remove all of the extranneous sub-tags - we only care about strings.
        holdingHeaderList = [filter(lambda x: isinstance(x, element.NavigableString), e.contents) for e in holdingHeaderTags]

        # Convert the NavigableStrings into actual strings
        holdingHeaderStrings = [[unicode(i).encode('ascii','ignore') for i in l] for l in holdingHeaderList]
        # Join the sub-list strings with spaces to get a list of combined strings
        holdingHeaderStrings = [' '.join(i) for i in holdingHeaderStrings]
        # Remove all the extra whitespace from any of these strings.
        holdingHeaderStrings = [' '.join(s.split()) for s in holdingHeaderStrings]
        # Filter out empty strings - they're falsy
        holdingHeaderStrings = filter(lambda x: x, holdingHeaderStrings)

        # print "\nHeader:"
        # print holdingHeaderStrings, len(holdingHeaderStrings)

        # Using an OrderedDict to keep the sorting order from the website.
        for row in holdingRowStrings:
            # For all of the data in this table,
            for index in range(1, len(row)):
                # Add it to the existing data - it will match by the name (element 1)
                holdingData[row[0]][holdingHeaderStrings[index]] = row[index]

        # print '\nData Header:'
        # # Print the holding data keys to compare.
        # for holding in holdingData.keys():
        #     print holdingData[holding].keys()

        return {v['Ticker']: v['% Portfolio Weight'] for (k, v) in holdingData.items()}