import dash
import dash_core_components as dcc 
import dash_html_components as html 
import dash_table

# Things to do - 
# dark theme
# buttons to select optimisation parameters
# better representation of coefficients



def app_layout2(good_ticker_dict,degree_options):
    return html.Div(style={
        'backgroundColor':'#303030'
    },children=[
        dcc.Store(id='ticker_store'),
        dcc.Store(id='smacs'),
        dcc.Store(id='coefs1'),
        dcc.Store(id='stats'),
        html.H1(children='SMA Cross & Momentum Optimiser',
        style={'textAlign':'center','color':'white'}),
        html.Div(className='row',children=[
            html.Div(className='four columns', children=[
                html.Label(['Select Stock'],style={'text-align':'center','color':'white'}),
                dcc.Dropdown(
                id='ticker_dropdown',
                options=good_ticker_dict,
                value='AZN',
                style={'color':'#303030'}), 
            ]),
            html.Div(className='four columns', children=[
                html.Label(['Select Degree'],style={'text-align':'center','color':'white'}),
                dcc.Dropdown(
                id='degrees',
                options=degree_options,
                value=4), 
            ]),
        ],style=dict(display='flex')),
            html.Div([
                html.Div([
                    dcc.Loading(id='load_1',children=html.Div(dcc.Graph(id='my_fig')), type='default')],
                    className='six columns'),
                html.Div([
                    dcc.Loading(id='load_2',children=html.Div(dcc.Graph(id='my_fig1')), type='default')],
                    className='six columns'),
                    ],className='row'),
            html.Div([
                html.Div([
                    dcc.Loading(id='load_3',children=html.Div(dcc.Graph(id='my_fig3')), type='default')],
                    className='six columns'),
                html.Div([
                    dcc.Loading(id='load_4',children=html.Div(dcc.Graph(id='my_fig4')), type='default')],
                    className='six columns'),
                    ],className='row'),
                html.Div([html.H3(['SMA Cross'])]),
                html.Button('Run Backtest Optimiser', id='optimiser'),
                dcc.Loading(id='load_5',children=html.Div(dcc.Graph(id='my_fig5')), type='default'),
                # dcc.Loading(id='load_6',children=html.Div(dcc.Graph(id='my_fig6')), type='default'),
                html.Div(style={'margin':"15px"},children=[html.H5('Line Fit Co-Efficients',style={'color':'white'}),
                dash_table.DataTable(id='coef-dash-table')]),
                html.Div(style={'margin':'15px'},children=[html.H5('SMA Cross Optimal',style={'color':'white'}),
                html.Div(style={'padding_left':'25%','padding_right':'25%'},children=[dash_table.DataTable(id='smac-dash-table')])]),
                html.Div(style={'margin':"15px"},children=[html.H5('Backtest Signalled Trades',style={'color':'white'}),
                dash_table.DataTable(id='trades-dash-table')])
    ])
