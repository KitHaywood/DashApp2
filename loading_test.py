import dash
import dash_core_components as dcc 
import dash_html_components as html
# from apps.template import app_layout, app_layout2 
from apps.utils import get_ticker_dict, get_ticker_data_2
import numpy as np 
import pandas as pd
import plotly.express as px 
import json
from apps.app import dash_app
from dash.dependencies import Input, Output, State


def app_layout(good_ticker_dict, degree_options):
    return html.Div(children=[
        html.H1(children='Test Yahoo Finance Fetcher',
        style={'textAlign':'center'}),
        html.Div(className='row',children=[
            html.Div(className='four columns', children=[
                html.Label(['Select Stock'],style={'text-align':'center'}),
                dcc.Dropdown(
                id='ticker_dropdown',
                options=good_ticker_dict,
                value='AZN'), 
            ]),
            html.Div(className='four columns', children=[
                html.Label(['Select Degree'],style={'text-align':'center'}),
                dcc.Dropdown(
                id='degrees',
                options=degree_options,
                value=4), 
            ]),
        ],style=dict(display='flex')),
        html.Div([
            dcc.Loading(children=html.Div(
                dcc.Graph(id='graph')),id='loader',type='default')
                ])
        ])
with open('apps/good_tickerdict.json') as g:
    good_ticker_dict = json.load(g)
degree_options = [{'label':x,'value':x} for x in range(1,10)]
dash_app = dash_app
dash_app.layout = app_layout(good_ticker_dict, degree_options)
@dash_app.callback(
        Output(component_id='graph', component_property='figure'),
        [Input(component_id='ticker_dropdown', component_property='value'),
        Input(component_id='degrees',component_property='value')]
        )
def update_line_chart(ticker,degree):
    good_data = get_ticker_data_2(ticker)
    try:
        good_data['time'] = good_data.index  
        start = good_data['time'][0]
        time = np.array([pd.Timedelta(x-start).total_seconds() for x in good_data['time']])
        fig1 = px.scatter(good_data,x='time',y='Open',template='simple_white',title='Time Series')
        fig1.update_traces(marker={'size': 4})
    except:
        None
    return fig1
    
if __name__=="__main__":
    dash_app.run_server(debug=True)
