from dash.dependencies import Input, Output, State
# import dash_bootstrap_components as dbc 
import dash
import dash_core_components as dcc 
import dash_html_components as html
from yahoo_finance_api2 import exceptions 
import pandas as pd 
from plotly.graph_objects import Scatter
from backtesting import Backtest
import dash_table
import numpy as np
import plotly.express as px 
import json
from apps.utils import get_ticker_dict, get_ticker_data_2, make_good_ticker_dict, SMA, SmaCross
from apps.app import dash_app
from apps.template import app_layout2
import concurrent.futures
import ast

# Options
# Vyper
# Solidity

# Things to do:
# - sort background colors for loading graphs

def get_data_table(coef1):
    data_table = dash_table.DataTable(
        id='coef-data-table',
        data=coef1['coefs'],
        columns = [{'id':x[0],'name':x[0]} for x in enumerate(coef1)],
    )
    return data_table

with open('apps/good_tickerdict.json') as g:
    good_ticker_dict = json.load(g)
degree_options = [{'label':x,'value':x} for x in range(1,10)]
dash_app = dash_app
dash_app.layout = app_layout2(good_ticker_dict, degree_options)
app = dash_app.server


@dash_app.callback(
    Output(component_id='ticker_store',component_property='data'),
    Input(component_id='ticker_dropdown', component_property='value'),
)
def get_data(ticker):
    data = get_ticker_data_2(ticker)
    data['time'] = data.index
    start = data['time'].iloc[0]
    time = np.array([pd.Timedelta(x-start).total_seconds() for x in data['time']])
    data['new_time'] = time
    return data.to_json(orient='records')


@dash_app.callback(
    Output(component_id='my_fig',component_property='figure'),
    Input(component_id='ticker_store', component_property='data')
)
def update_time_series(data):
    data = pd.read_json(data)
    # print(data.new_time.head(20))
    fig = px.scatter(data,x='new_timestamp',y='Open',template='simple_white',title='Time Series')
    fig.update_layout(paper_bgcolor="#303030",plot_bgcolor='#303030',font={'color':'white'})
    return fig


@dash_app.callback(
    [Output(component_id='my_fig5', component_property='figure'),
    Output(component_id='smacs', component_property='data'),
    Output(component_id='stats',component_property='data')],
    Input(component_id='ticker_store', component_property='data')    
)
def update_backtest_chart(data):
    data = pd.read_json(data)
    bt = Backtest(data, SmaCross, cash=10_000, commission=0.02, hedging=True)

    def maximiser(series):
        """takes series result of bt and returns a 
        float which maximises return and minimises num of trades"""
        return series['Equity Final [$]'] if 0 <= series['# Trades'] <= 10 else 0

    stats = bt.optimize(n1=range(5, 51, 3),
            n2=range(10, 210, 3),
            maximize=maximiser,
            constraint=lambda param: param.n1 < param.n2)
    # print('\n','Trades: ',stats['# Trades'],'\n')
    eq_curve = stats._equity_curve
    eq_curve['time'] = eq_curve.index    
    fig5 = px.line(eq_curve,x='time',y='Equity',template='simple_white')
    fig5.update_layout(paper_bgcolor="#303030",plot_bgcolor='#303030',font={'color':'white'})
    smac = {'sma1':stats._strategy.n1,'sma2':stats._strategy.n2}
    stats = stats['_trades'].to_json(orient='records')
    return fig5, smac, stats


@dash_app.callback(
    [Output(component_id='my_fig1',component_property='figure'),
    Output(component_id='coefs1', component_property='data')],
    [Input(component_id='ticker_store', component_property='data'),
    Input(component_id='smacs', component_property='data'),
    Input(component_id='degrees',component_property='value')]
)
def update_fit(data,smacs,degree):
    data = pd.read_json(data)
    start = data['time'][0]    
    time = np.array([pd.Timedelta(x-start).total_seconds() for x in data['time']])
    coefs = np.polyfit(time,np.nan_to_num(np.array(SMA(data['Open'],smacs['sma1']))),degree)
    coef_df = pd.DataFrame.from_dict({'time':time,
                                            'coeffs':np.polyval(coefs,time),
                                            'original_t':data['time']})
    fig2 = px.line(coef_df,x='original_t',y='coeffs', template='simple_white',title='Polynomial Fit')
    fig2.update_layout(paper_bgcolor="#303030",plot_bgcolor='#303030',font={'color':'white'})
    coef1 = {'coefs':coefs}
    print(type(coef1['coefs']))
    # coef1 = [{x[0]:x[1]} for x in enumerate(coefs)]
    return fig2, coef1


@dash_app.callback(
    Output(component_id='my_fig3',component_property='figure'),
    [Input(component_id='ticker_store',component_property='data'),
    Input(component_id='coefs1', component_property='data')]
)
def update_der1(data,coefs):
    data = pd.read_json(data)
    start = data['time'][0]
    time = np.array([pd.Timedelta(x-start).total_seconds() for x in data['time']])
    der1 = np.polyder(coefs['coefs'],1)
    der1_df = pd.DataFrame.from_dict({'time':time,
                                            'der1':np.polyval(der1,time),
                                            'original_t':data['time']})
    fig3 = px.line(der1_df,x='original_t',y='der1',template='simple_white',title='First Derivative')
    fig3.update_layout(paper_bgcolor="#303030",plot_bgcolor='#303030',font={'color':'white'})
    return fig3


@dash_app.callback(
    Output(component_id='my_fig4',component_property='figure'),
    [Input(component_id='ticker_store',component_property='data'),
    Input(component_id='coefs1',component_property='data')]
)
def update_der2(data,coefs):
    data = pd.read_json(data)
    start = data['time'][0]
    time = np.array([pd.Timedelta(x-start).total_seconds() for x in data['time']])
    der2 = np.polyder(coefs['coefs'],2)
    der2_df = pd.DataFrame.from_dict({'time':time,
                                            'der2':np.polyval(der2,time),
                                            'original_t':data['time']})
    fig4 = px.line(der2_df,x='original_t',y='der2',template='simple_white',title='Second Derivative')
    fig4.update_layout(paper_bgcolor="#303030",plot_bgcolor='#303030',font={'color':'white'})
    return fig4

@dash_app.callback(
    [Output(component_id='coef-dash-table',component_property='data'),
    Output(component_id='coef-dash-table',component_property='columns')],
    Input(component_id='coefs1', component_property='data')
)
def update_coef_table(coef1):
    '''takes coef dict and returns columns as list of dict and data as list of dict of id:num'''
    columns = [{'id':f"x ^^ {str(x[0])}",'name':f'x ^^ {str(x[0])}'} for x in enumerate(coef1['coefs'])]
    data = [{f"x ^^ {str(x[0])}":x[1] for x in enumerate(coef1['coefs'])}]
    return data,columns

@dash_app.callback(
    [Output(component_id='smac-dash-table',component_property='data'),
    Output(component_id='smac-dash-table',component_property='columns')],
    Input(component_id='smacs', component_property='data')
)
def update_smac_table(smacs):
    '''makes table for sma1 and sma2'''
    columns = [{'id':str(k),'name':str(k)} for k,x in smacs.items()]
    data = [{str(k):x for k,x in smacs.items()}]
    return data, columns

@dash_app.callback(
    [Output(component_id='trades-dash-table',component_property='data'),
    Output(component_id='trades-dash-table',component_property='columns')],
    Input(component_id='stats',component_property='data')
)
def update_trades_table(stats):
    pre_data = pd.read_json(stats)
    columns = [{'id':str(x),'name':str(x)} for x in pre_data.columns]
    print('i got here 2')
    data = pre_data.to_dict(orient='records')
    print('i got here 3')
    return data,columns



# @dash_app.callback(
#     [Output(component_id='coefs',component_property='children'),
#     Output(component_id='smac',component_property='children')],
#     [Input(component_id='smacs',component_property='data'),
#     Input(component_id='coefs1',component_property='data')]
# )
# def update_text_data(smacs, coefs1):
#     smacs = f"sma1: {smacs['sma1']} - - sma2: {smacs['sma2']}"
#     coefs1 = coefs1['coefs']
#     return coefs1, smacs

if __name__=="__main__":
    dash_app.run_server(host='0.0.0.0',threaded=True, debug=True, port=8080)
