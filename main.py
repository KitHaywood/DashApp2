from dash.dependencies import Input, Output, State
# import dash_bootstrap_components as dbc 
import dash
import dash_core_components as dcc 
import dash_html_components as html
from yahoo_finance_api2 import exceptions 
import pandas as pd 
from plotly.graph_objects import Scatter
from backtesting import Backtest
import numpy as np
import plotly.express as px 
import json
from apps.utils import get_ticker_dict, get_ticker_data_2, make_good_ticker_dict, SMA, SmaCross
from apps.app import dash_app
from apps.template import app_layout2
import concurrent.futures
import ast

with open('apps/good_tickerdict.json') as g:
    good_ticker_dict = json.load(g)
degree_options = [{'label':x,'value':x} for x in range(1,10)]
dash_app = dash_app
dash_app.layout = app_layout2(good_ticker_dict, degree_options)
app = dash_app.server
# Now need to make callbacks for individual graphs to load individuall

@dash_app.callback(
     [Output(component_id='my_fig',component_property='figure'),
     Output(component_id='my_fig1', component_property='figure'),
     Output(component_id='my_fig3', component_property='figure'),
     Output(component_id='my_fig4', component_property='figure')],
     [Input(component_id='ticker_dropdown', component_property='value'),
        Input(component_id='degrees',component_property='value')]
        )
def update_fit_chart(ticker,degree):
    good_data = get_ticker_data_2(ticker)
    good_data['time'] = good_data.index  
    start = good_data['time'][0]
    time = np.array([pd.Timedelta(x-start).total_seconds() for x in good_data.index])
    fig1 = px.scatter(good_data,x='time',y='Open',template='simple_white',title='Time Series')
    fig1.update_traces(marker={'size': 4})
    coefs = np.polyfit(time,np.nan_to_num(np.array(SMA(good_data['Open'],stats._strategy.n1))),degree)
    coef_df = pd.DataFrame.from_dict({'time':time,
                                        'coeffs':np.polyval(coefs,time),
                                        'original_t':good_data['time']})
    fig2 = px.line(coef_df,x='original_t',y='coeffs', template='simple_white',title='Polynomial Fit')
    der1 = np.polyder(coefs,1)
    der2_df = pd.DataFrame.from_dict({'time':time,
                                            'der2':np.polyval(der2,time),
                                            'original_t':good_data['time']})
    fig3 = px.line(der1_df,x='original_t',y='der1',template='simple_white',title='First Derivative')
    der2 = np.polyder(coefs,2)
    der2_df = pd.DataFrame.from_dict({'time':time,
                                            'der2':np.polyval(der2,time),
                                            'original_t':good_data['time']})
    fig4 = px.line(der2_df,x='original_t',y='der2',template='simple_white',title='Second Derivative')
    return fig1, fig2, fig3, fig4

@dash_app.callback(
        [Output(component_id='my_fig5', component_property='figure'),
        Output(component_id='my_fig6',component_property='figure'),
        Output(component_id='coefs',component_property='children'),
        Output(component_id='smac',component_property='children')],
        [Input(component_id='optimiser',component_property='n_clicks'),
        Input(component_id='ticker_dropdown', component_property='value'),
        Input(component_id='degrees',component_property='value')])
def run_backtester(ticker, degree, n_ticks):
    good_data = get_ticker_data_2(ticker)
    good_data['time'] = good_data.index  
    start = good_data['time'][0]
    time = np.array([pd.Timedelta(x-start).total_seconds() for x in good_data['time']])
    bt = Backtest(good_data, SmaCross, cash=10_000, commission=.002)
    stats = bt.optimize(n1=range(5, 50, 5),
            n2=range(10, 200, 5),
            maximize='Equity Final [$]',
            constraint=lambda param: param.n1 < param.n2)
    eq_curve = stats._equity_curve
    eq_curve['time'] = eq_curve.index
    fig5 = px.line(eq_curve,x='time',y='Equity',template='simple_white')
    fig1 = px.scatter(good_data,x='time',y='Open',template='simple_white',title='Time Series')
    fig1.update_traces(marker={'size': 4})
    fig1.add_trace(Scatter(x=good_data['time'],y=SMA(good_data['Open'],stats._strategy.n1),name='Short MA'))
    fig1.add_trace(Scatter(x=good_data['time'],y=SMA(good_data['Open'],stats._strategy.n2),name='Long MA'))
    return fig5, fig1

if __name__=="__main__":
    dash_app.run_server(host='0.0.0.0',debug=True, port=8080)


# @dash_app.callback(
#         [Output(component_id='my_fig', component_property='figure'),
#         Output(component_id='my_fig2', component_property='figure'),
#         Output(component_id='my_fig3', component_property='figure'),
#         Output(component_id='my_fig4', component_property='figure'),
#         Output(component_id='my_fig5', component_property='figure'),
#         Output(component_id='coefs',component_property='children'),
#         Output(component_id='smac',component_property='children')],
#         [Input(component_id='ticker_dropdown', component_property='value'),
#         Input(component_id='degrees',component_property='value')]
#         )
# def update_line_chart(ticker,degree):
#     good_data = get_ticker_data_2(ticker)
#     # print(good_data)
#     try:
#         good_data['time'] = good_data.index  
#         start = good_data['time'][0]
#         time = np.array([pd.Timedelta(x-start).total_seconds() for x in good_data['time']])
#         fig1 = px.scatter(good_data,x='time',y='Open',template='simple_white',title='Time Series')
#         fig1.update_traces(marker={'size': 4})
#         bt = Backtest(good_data, SmaCross, cash=10_000, commission=.002)
#         stats = bt.optimize(n1=range(5, 50, 5),
#                 n2=range(10, 200, 5),
#                 maximize='Equity Final [$]',
#                 constraint=lambda param: param.n1 < param.n2)
#         eq_curve = stats._equity_curve
#         eq_curve['time'] = eq_curve.index
#         fig5 = px.line(eq_curve,x='time',y='Equity',template='simple_white')
#         smac = str(stats._strategy)
#         fig1.add_trace(Scatter(x=good_data['time'],y=SMA(good_data['Open'],stats._strategy.n1),name='Short MA'))
#         fig1.add_trace(Scatter(x=good_data['time'],y=SMA(good_data['Open'],stats._strategy.n2),name='Long MA'))

#         # print(np.nan_to_num(np.array(SMA(good_data['Open'],stats._strategy.n1))))
#         coefs = np.polyfit(time,np.nan_to_num(np.array(SMA(good_data['Open'],stats._strategy.n1))),degree)
#         # print(coefs)
#         # print(np.polyval(time,coefs))
#         coef_df = pd.DataFrame.from_dict({'time':time,
#                                             'coeffs':np.polyval(coefs,time),
#                                             'original_t':good_data['time']})
#         fig2 = px.line(coef_df,x='original_t',y='coeffs', template='simple_white',title='Polynomial Fit')
#         der1 = np.polyder(coefs,1)
#         # print('der1: ',der1)
#         der1_df = pd.DataFrame.from_dict({'time':time,
#                                             'der1':np.polyval(der1,time),
#                                             'original_t':good_data['time']})
#         fig3 = px.line(der1_df,x='original_t',y='der1',template='simple_white',title='First Derivative')
#         der2 = np.polyder(coefs,2)
#         # print('der2: ',der2) 
#         der2_df = pd.DataFrame.from_dict({'time':time,
#                                             'der2':np.polyval(der2,time),
#                                             'original_t':good_data['time']})
#         fig4 = px.line(der2_df,x='original_t',y='der2',template='simple_white',title='Second Derivative')


#         coefs = np.polyfit(time,np.array(good_data['Open']),degree)
#         # print('coefs: ',coefs)
#         coef_df = pd.DataFrame.from_dict({'time':time,
#                                             'coeffs':np.polyval(coefs,time),
#                                             'originc
#         fig1,fig2,fig3,fig4,fig5 = 'No Ticker Available'
#     return fig1, fig2, fig3, fig4, fig5, coefs, smac

# @dash_app.callback(
#     [Output(component_id='my_fig', component_property='figure')],
#     [Input(component_id='ticker_dropdown', component_property='value')]
# )
# def update_timeseries()
# good_data = get_ticker_data_2(ticker)
# time = np.array([pd.Timedelta(x-start).total_seconds() for x in good_data['time']])

# @dash_app.callback(
#      Output(component_id='my_fig',component_property='figure'),
#      [Input(component_id='ticker_dropdown', component_property='value'),
#         Input(component_id='degrees',component_property='value')]) ;
# def update_time_series_chart(ticker,degree,good_data=good_data):
#     good_data = get_ticker_data_2(ticker)
#     try:
#         good_data['time'] = good_data.index  
#         start = good_data['time'][0]
#         time = np.array([pd.Timedelta(x-start).total_seconds() for x in good_data['time']])
#         fig1 = px.scatter(good_data,x='time',y='Open',template='simple_white',title='Time Series')
#         fig1.update_traces(marker={'size': 4})
#     except:
#         None
#     return fig1

# @dash_app.callback(
#      Output(component_id='my_fig',component_property='figure'),
#      [Input(component_id='ticker_dropdown', component_property='value'),
#         Input(component_id='degrees',component_property='value')])
# def update_backtest_chart(ticker,degree,good_data=good_data):

# ArgParser
# FISHING APP
# Directions, Calendar Integration, Nearby Amenities, Interactive River Guide, Recommended Fishing Tackle?
# Group Message Capabilities (?), 
# with open('apps/tickerdict.json','r') as f:
#     tickerdict = json.load(f)

# with concurrent.futures.ThreadPoolExecutor() as exec:
#     results = {x['value']:exec.submit(get_ticker_data_2,x['value']) for x in tickerdict}
# results = {k:v.result() for k,v in results.items()}

# results = {k:v.dropna() for k,v in results.items() if v is not None}

