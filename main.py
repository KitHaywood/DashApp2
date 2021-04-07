from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc 
import dash_html_components as html
from yahoo_finance_api2 import exceptions 
import pandas as pd 
from plotly.graph_objects import Scatter
from backtesting import Backtest
import numpy as np
import plotly.express as px 

from apps.utils import get_ticker_dict, get_ticker_data_2, make_good_ticker_dict, SMA, SmaCross
from apps.app import dash_app
from apps.template import app_layout
import concurrent.futures

tickerdict = get_ticker_dict()
with concurrent.futures.ThreadPoolExecutor() as exec:
    results = {x['value']:exec.submit(get_ticker_data_2,x['value']) for x in tickerdict}
results = {k:v.result() for k,v in results.items()}
results = {k:v.dropna() for k,v in results.items() if v is not None}
good_ticker_dict = make_good_ticker_dict(tickerdict,results)
degree_options = [{'label':x,'value':x} for x in range(1,10)]

app = dash_app.server
@dash_app.callback(
        [Output(component_id='my_fig', component_property='figure'),
        Output(component_id='my_fig2', component_property='figure'),
        Output(component_id='my_fig3', component_property='figure'),
        Output(component_id='my_fig4', component_property='figure'),
        Output(component_id='my_fig5', component_property='figure'),
        Output(component_id='coefs',component_property='children'),
        Output(component_id='smac',component_property='children')],
        [Input(component_id='ticker_dropdown', component_property='value'),
        Input(component_id='degrees',component_property='value')]
        )
def update_line_chart(ticker,degree):
    good_data = results[ticker]
    try:
        good_data['time'] = good_data.index  
        start = good_data['time'][0]
        time = np.array([pd.Timedelta(x-start).total_seconds() for x in good_data['time']])
        fig1 = px.scatter(good_data,x='time',y='Open',template='simple_white',title='Time Series')
        fig1.update_traces(marker={'size': 4})
        bt = Backtest(results[ticker], SmaCross, cash=10_000, commission=.002)
        stats = bt.optimize(n1=range(5, 50, 5),
                n2=range(10, 200, 5),
                maximize='Equity Final [$]',
                constraint=lambda param: param.n1 < param.n2)
        eq_curve = stats._equity_curve
        eq_curve['time'] = eq_curve.index
        fig5 = px.line(eq_curve,x='time',y='Equity',template='simple_white')
        smac = str(stats._strategy)
        fig1.add_trace(Scatter(x=good_data['time'],y=SMA(good_data['Open'],stats._strategy.n1),name='Short MA'))
        fig1.add_trace(Scatter(x=good_data['time'],y=SMA(good_data['Open'],stats._strategy.n2),name='Long MA'))

        print(np.nan_to_num(np.array(SMA(good_data['Open'],stats._strategy.n1))))
        coefs = np.polyfit(time,np.nan_to_num(np.array(SMA(good_data['Open'],stats._strategy.n1))),degree)
        print(coefs)
        print(np.polyval(time,coefs))
        coef_df = pd.DataFrame.from_dict({'time':time,
                                            'coeffs':np.polyval(coefs,time),
                                            'original_t':good_data['time']})
        fig2 = px.line(coef_df,x='original_t',y='coeffs', template='simple_white',title='Polynomial Fit')
        der1 = np.polyder(coefs,1)
        print('der1: ',der1)
        der1_df = pd.DataFrame.from_dict({'time':time,
                                            'der1':np.polyval(der1,time),
                                            'original_t':good_data['time']})
        fig3 = px.line(der1_df,x='original_t',y='der1',template='simple_white',title='First Derivative')
        der2 = np.polyder(coefs,2)
        print('der2: ',der2) 
        der2_df = pd.DataFrame.from_dict({'time':time,
                                            'der2':np.polyval(der2,time),
                                            'original_t':good_data['time']})
        fig4 = px.line(der2_df,x='original_t',y='der2',template='simple_white',title='Second Derivative')


        coefs = np.polyfit(time,np.array(good_data['Open']),degree)
        print('coefs: ',coefs)
        coef_df = pd.DataFrame.from_dict({'time':time,
                                            'coeffs':np.polyval(coefs,time),
                                            'original_t':good_data['time']})
    except exceptions.YahooFinanceError:
        fig1,fig2,fig3,fig4,fig5 = 'No Ticker Available'
    return fig1, fig2, fig3, fig4, fig5, coefs, smac

if __name__=="__main__":
    dash_app.run_server(host='0.0.0.0',debug=True, port=8080)