from yahooquery import Ticker
import pandas as pd
import Util as ut

class dataticker():

    def hist_price(self , ticker , start = None , end = None , interval = '1d'):
        if end is None and start is None:
            raise ValueError('Requires at value for start or end')
        if start is None:
            raise ValueError('Requires value for start')
        stockyq = Ticker(ticker)
        price = stockyq.history(interval = interval , start = start , end = end)
        #price.to_excel("price.xlsx")
        return price
    
    def clean_hist(self , ticker , start = None , end = None , interval = '1d'):
        df = self.hist_price(ticker = ticker, start = start, end = end , interval = interval)
        df = ut.multi_to_single(df , 'symbol')
        ut.clean(df , cols = ['symbol' , 'dividends' , 'adjclose'])
        df.index = df.index.map(str)
        return df
        
"""
def main():
    
    strat = Strategy()
    macd = Macd.Macd("MSFT" , length = 50)
    macd_ind = macd.indicator()
    print(strat.decision(macd_ind , macd_ind['MACD_12_26_9'] , macd_ind['MACDS_12_26_9']))

if __name__ == '__main__':
    main()
"""