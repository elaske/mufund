mufund
======

Most of my portfolio is in mutual funds rather than individual stocks. This allows me to diversify a bit more easily without the added cost of trading. Also, it doesn't open yourself up to as much volatility as ETFs can experience, since they're subject to the whims of market emotions just the same as individual stocks.

Mutual funds have one very big problem, though: you do not know the share price at which you're going to be buying and selling them like stocks. With stocks, you list a price you want to buy / sell at and your broker makes sure you pay / get paid exactly that (after taking a commission, of course). You have to buy into mutual funds (slightly different than purchasing a share of stock), and have to initiate it during trading hours, usually. Mutual funds have their prices set (actually called a NAV), some time after the close of the market, however - usually around when people leave for the day.

Setting aside the reasons why this is the case (which I understand and am not arguing with at all), this makes buying into and cashing out of mutual funds relatively risky. One nice thing about mutual funds is that they publish their holdings (at least to some people looking to sell that data). The top 10 are freely available at places like Google and Yahoo!; however, Morningstar displays to users up to 25 (they try to charge for the top 100).

You can start to predict what the prices of the mutual funds are going to do based on the holdings did that day. If all of the holdings went up 1%, the NAV of the mutual fund will tend to go up 1%. This correlation is less descriptive of funds which you know less of the total composition (say they had 300 positions total), have a higher turnover rate (buying and selling of their positions a lot), or are leveraged (borrowing in order to buy in extra).

This is what this script is meant to do: It takes the mutual fund ticker, grab the holding and composition data from Morningstar, and then will attempt to get the information about all of the holdings and predict a percentage increase. 

There are some inaccuracies in this, of course. In addition to the ones listed above, there's also the fact that bond prices / yields aren't always published individually, so funds have hold bonds aren't very well predicted. Also, mutual funds only usually publish their holdings quarterly, so as the quarter goes on, the holding percentages might change, but this can only predict based on the data known from the last publishing.