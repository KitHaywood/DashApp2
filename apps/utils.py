import yahoo_finance_api2 as yf 
from yahoo_finance_api2 import share
import requests
import pandas as pd 
import datetime as dt 
from dash.dependencies import Input, Output
from yahoo_finance_api2 import exceptions
import concurrent.futures
from backtesting import Strategy
from backtesting import Backtest
from backtesting.lib import crossover


def get_ticker_dict():
    """returns dict of ticker prepared for dropdown"""
    url = 'https://en.wikipedia.org/wiki/FTSE_100_Index#cite_note-13'
    html = requests.get(url).content
    df_list = pd.read_html(html)[3]
    tickerdict = [{'label':x['Company'],'value':x['EPIC']} for idx,x in df_list.iterrows()]
    return tickerdict

def get_ticker_data_2(ticker):
    """takes ticker code such as 'AZN' and returns a dataframe of
    OCHLV"""
    my_share = share.Share(ticker)
    try:
        data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                                        100,
                                                        share.FREQUENCY_TYPE_MINUTE,
                                                        30)                                               
        if data is not None:
            df = pd.DataFrame.from_dict(data)
            df['new_timestamp'] = [dt.datetime.fromtimestamp(x/1000) for x in df['timestamp']]
            df = df.set_index('timestamp')
            df.columns = ['Open','High','Low','Close','Volume','new_timestamp']
            if df.isnull().values.any():
                df = df.interpolate(method='linear',axis=0)
            return df
        else:
            print('No Data from YahooFinance')     
            return None
    except exceptions.YahooFinanceError:
        pass

def make_good_ticker_dict(tickerdict,results):
    res = [x for x in tickerdict if x['value'] in results.keys()]
    return res

def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).rolling(n).mean()

def num_trades(values):
    return pd.Series([x for x in range(len(values))])
class SmaCross(Strategy):
    """Define the two MA lags as *class variables*
    for later optinmization"""
    n1 = 10
    n2 = 20

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
        # print(self.data)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()