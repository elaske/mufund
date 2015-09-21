# Google Finance Notes

Google Finance includes all of the quote data in special tags as part of it's "+1" button. This must enable them to share all of the data without having to scrape their own pages.
This might be easier to use to gather the data from.

Here are a couple examples:

**FBIOX:**

```
<div id="sharebox-data" itemscope="itemscope" itemtype="http://schema.org/Intangible/FinancialQuote">
<meta itemprop="name" content="Fidelity Select Biotechnology Portfolio">
<meta itemprop="url" content="https://www.google.com/finance?cid=637054626025607">
<meta itemprop="imageUrl" content="https://www.google.com/finance/chart?cht=g&amp;q=MUTF:FBIOX&amp;tkr=1&amp;p=1M&amp;enddatetime=2014-02-28T21:00:00Z">
<meta itemprop="tickerSymbol" content="FBIOX">
<meta itemprop="exchange" content="MUTF">
<meta itemprop="exchangeTimezone" content="America/New_York">
<meta itemprop="price" content="221.48">
<meta itemprop="priceChange" content="-6.96">
<meta itemprop="priceChangePercent" content="-3.05">
<meta itemprop="quoteTime" content="2014-02-28T21:00:00Z">
<meta itemprop="dataSource" content="">
<meta itemprop="dataSourceDisclaimerUrl" content="//www.google.com/intl/en-US/googlefinance/disclaimer">
<meta itemprop="priceCurrency" content="USD">
</div>
```

**REGENERON PHARMACEUTICALS INC:**

```
<div id="sharebox-data" itemscope="itemscope" itemtype="http://schema.org/Intangible/FinancialQuote">
<meta itemprop="name" content="Regeneron Pharmaceuticals Inc">
<meta itemprop="url" content="https://www.google.com/finance?cid=479891">
<meta itemprop="imageUrl" content="https://www.google.com/finance/chart?cht=g&amp;q=NASDAQ:REGN&amp;tkr=1&amp;p=1d&amp;enddatetime=2014-02-28T21:00:00Z">
<meta itemprop="tickerSymbol" content="REGN">
<meta itemprop="exchange" content="NASDAQ">
<meta itemprop="exchangeTimezone" content="America/New_York">
<meta itemprop="price" content="332.50">
<meta itemprop="priceChange" content="-6.04">
<meta itemprop="priceChangePercent" content="-1.78">
<meta itemprop="quoteTime" content="2014-02-28T21:00:00Z">
<meta itemprop="dataSource" content="NASDAQ real-time data">
<meta itemprop="dataSourceDisclaimerUrl" content="//www.google.com/help/stock_disclaimer.html#realtime">
<meta itemprop="priceCurrency" content="USD">
</div>
```

---

# Transaction Types:
- **Investment (Deposit)**: From outside source
  - Amount = -X
- **Withdrawal**: To outside source
  - Amount = +X
- **Purchase**: From available cash
  - Amount = -(X*Y)
  - Price  = +X
  - Shares = -Y
- **Sale**: To available cash
  - Amount = +(X*Y)
  - Price  = +X
  - Shares = +Y
- **Distribution**: To available cash
  - Amount = +X
- **Reinvestment**: Just another purchase
- **Split**: Adds to the number of shares
  - Amount = 0
  - Shares = +X
  - Price  = 0
