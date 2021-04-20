import dash
import dash_core_components as dcc 
import dash_html_components as html 

def app_layout(good_ticker_dict,degree_options):
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
                html.Div([
                    dcc.Loading(children=[html.Div(dcc.Graph(id='my_fig'))],id='my_fig_loading1',type='default')],
                    className='six columns'),
                html.Div([
                    dcc.Loading(children=[html.Div(dcc.Graph(id='my_fig2'))],id='my_fig_loading2',type='default')],
                    className='six columns'),
                    ],className='row'),
            html.Div([
                html.Div([
                    dcc.Loading(children=[html.Div(dcc.Graph(id='my_fig3'))],id='my_fig_loading3',type='default')],
                    className='six columns'),
                html.Div([
                    dcc.Loading(children=[html.Div(dcc.Graph(id='my_fig4'))],id='my_fig_loading4',type='default')],
                    className='six columns'),
                    ],className='row'),
                html.Div([html.H3(['SMA Cross'])]),
                dcc.Loading(children=[html.Div(dcc.Graph(id='my_fig5'))],id='my_fig_loading5',type='default'),
                html.H5('Line Fit Co-Efficients'),
                html.P(id='coefs'),
                html.H5('SMA Cross Optimal'),
                html.P(id='smac')
    ])
