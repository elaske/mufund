#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: elaske
# @Date:   2014-03-01 21:45:31
# @Last Modified by:   Evan Laske
# @Last Modified time: 2014-03-01 22:56:45

import urllib
import urllib2
from bs4 import BeautifulSoup
import html5lib
import re

def main():
	ticker = "FBIOX"

	quoteURL = 'http://quotes.morningstar.com/fund/f?t='
	portfolioURL = 'http://portfolios.morningstar.com/fund/summary?t='
	holdingsURL = 'http://portfolios.morningstar.com/fund/holdings?t='
	googleFinanceURL = 'http://www.google.com/finance?q='

	print get_quote("goog")

def get_quote(symbol):
    base_url = 'http://finance.google.com/finance?q='
    content = urllib.urlopen(base_url + symbol).read()

    return [get_price(content), get_change(content), get_pct_change(content)]

def get_price(content):
    m = re.search('id="ref_[0-9]*_l".*?>(.*?)<', content)
    if m:
        price = m.group(1)
    else:
        price = 'no quote available for symbol'
    return price

def get_change(content):
    m = re.search('id="ref_[0-9]*_c".*?>(.*?)<', content)
    if m:
        change = m.group(1)
    else:
        change = 'no quote available for symbol'
    return change

def get_pct_change(content):
    m = re.search('id="ref_[0-9]*_cp".*?>(.*?)<', content)
    if m:
    	# Remove excess characters to make it a float.
        pct_change = m.group(1).strip('()%')
    else:
        pct_change = 'no quote available for symbol'
    return pct_change

# Standard main call
if __name__ == "__main__":
	main()