import dash
import dash_core_components as dcc 
import dash_html_components as html 


def app_layout():
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
                    dcc.Graph(id='my_fig')],
                    className='six columns'),
                html.Div([
                    dcc.Graph(id='my_fig2')],
                    className='six columns'),
                    ],className='row'),
            html.Div([
                html.Div([
                    dcc.Graph(id='my_fig3')],
                    className='six columns'),
                html.Div([
                    dcc.Graph(id='my_fig4')],
                    className='six columns'),
                    ],className='row'),
                html.Div([html.H3(['SMA Cross'])]),
                dcc.Graph(id='my_fig5'),
                html.H5('Line Fit Co-Efficients'),
                html.P(id='coefs'),
                html.H5('SMA Cross Optimal'),
                html.P(id='smac')
    ])
