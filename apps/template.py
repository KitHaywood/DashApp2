import dash
import dash_core_components as dcc 
import dash_html_components as html 
import dash_table

def app_layout2(good_ticker_dict,degree_options,max_trades):
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
        ],style={'display':'flex','margin':'15px'}),
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
                html.Div(style={'margin':'20px'},children=[
                html.Div([html.Button('Run Backtest Optimiser', id='optimiser')],className='four columns'),
                # html.Div(['Hello']),
                html.Div(children=[
                    html.Label(['Select Maximum Allowed Trades'],
                        style={'text-align':'center','color':'white'}),
                    dcc.Dropdown(
                        id='max_trades_dropdown',
                        options=max_trades,
                        value=10,
                        style={'color':'#303030'}
                        )
                    ],
                    className='four columns')],className='row'),
                dcc.Loading(id='load_5',children=html.Div(dcc.Graph(id='my_fig5')), type='default'),
                # dcc.Loading(id='load_6',children=html.Div(dcc.Graph(id='my_fig6')), type='default'),
                html.Div(style={'margin':"15px"},children=[
                        html.H5('Line Fit Co-Efficients',style={'color':'white'}),
                        dash_table.DataTable(
                            id='coef-dash-table',
                            style_table={
                                'border': '1px solid white',
                                'borderRadius': '15px',
                                'overflow': 'hidden'
                            },
                            style_header={
                                'backgroundColor':'rgb(30,30,30)',
                            },
                            style_cell={
                                'backgroundColor':'rgb(50,50,50)',
                                'color':'white',
                                'margin':'2px'
                            },)
                        ]),
                html.Div(style={'margin':'15px'},children=[
                    html.H5('SMA Cross Optimal',style={'color':'white'}),
                    html.Div(style={'margin':'55px'},children=[
                                dash_table.DataTable(
                                    id='smac-dash-table',
                                    style_table={
                                        'border': '1px solid white',
                                        'borderRadius': '15px',
                                        'overflow': 'hidden'
                                    },
                                    style_header={
                                        'backgroundColor':'rgb(30,30,30)'
                                    },
                                    style_cell={
                                        'backgroundColor':'rgb(50,50,50)',
                                        'color':'white',
                                        'margin':'20px'
                                    }
                                )
                            ])
                        ]),
                html.Div(style={
                    'margin':"15px",
                    'margin_bottom':'25px'
                    },
                    children=[
                    html.H5('Backtest Signalled Trades - $10,000 Starting',style={'color':'white'}),
                    dcc.Loading(id='trade_table_load',children=[dash_table.DataTable(
                    id='trades-dash-table',
                    style_table={
                        'border': '1px solid white',
                        'borderRadius': '15px',
                        'overflow': 'hidden'
                    },
                    style_header={'backgroundColor':'rgb(30,30,30)'},
                    style_cell={
                        'backgroundColor':'rgb(50,50,50)',
                        'color':'white',
                        'margin':'2px'
                    },
                    style_data_conditional=[
                        {'if':
                            {
                        'filter_query':'{ReturnPct} > 0',
                        # 'column_id':'ReturnPct'
                        },
                        'backgroundColor':'#3D9970',
                        'color':'white'
                    },
                    {
                        'if':
                        {
                            'filter_query':'{ReturnPct} < 0',
                        },
                        'backgroundColor':'#FF4136',
                        'color':'white'
                    }
                    ],
                    # style={'margin_bottom':'25px'}
                )])
                ]),
                html.Div(style={
                    'margin':'15px',
                },children=['hello'])
    ])
