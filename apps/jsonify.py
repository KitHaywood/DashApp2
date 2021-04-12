import json
from utils import get_ticker_dict,make_good_ticker_dict,get_ticker_data_2
import requests
import concurrent.futures
from pandas import read_html

def jsonify():
    """returns dict of ticker prepared for dropdown"""
    url = 'https://en.wikipedia.org/wiki/FTSE_100_Index#cite_note-13'
    html = requests.get(url).content
    df_list = read_html(html)[3]
    df_list = df_list[['Company','EPIC']]
    res = dict(df_list.values)
    # print(res)
    res = [{'label':k,'value':v} for k,v in res.items()]
    return res

if __name__=="__main__":

    tickerdict = jsonify()
    with concurrent.futures.ThreadPoolExecutor() as exec:
        results = {x['value']:exec.submit(get_ticker_data_2,x['value']) for x in tickerdict}
    results = {k:v.result() for k,v in results.items()}
    results = {k:v.dropna() for k,v in results.items() if v is not None}
    good_ticker_dict = make_good_ticker_dict(tickerdict,results)
    # with open('tickerdict.json','w+') as f:
    #     json.dump(tickerdict,f)
    with open('good_tickerdict.json','w+') as g:
        json.dump(good_ticker_dict)