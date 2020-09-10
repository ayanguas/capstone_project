# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 11:30:37 2020

@author: Albert Yanguas - ayanguasrovira@gmail.com
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from app import app
import handlers as hdlr #get_params, dark
import os

params = hdlr.get_params(hdlr.dark)

colors = params['colors']

# Evento para el refresco del grafico principal
GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", params['data_len'])

##############################################################################
#                              HOME LAYOUT                                   #
##############################################################################

home_layout = html.Div([
    html.Div([
        dbc.Card([
            dbc.CardHeader([
                html.H4('Resumen del proceso', className='text-style m-0'),
            ], className='', id='plant-plot-header'),
            dbc.CardBody([
                dcc.Graph(
                    id="plant-plot",
                    figure=dict(
                        layout=dict(
                            plot_bgcolor=colors["graph-bg"],
                            paper_bgcolor=colors["graph-bg"],
                        )
                    ),
                    style={"height": "100%"},
                ),
                dcc.Interval(
                    id="signal-update",
                    interval=int(GRAPH_INTERVAL),
                    n_intervals=0,
                )
            ], className='h-100')
        ], className='h-100', outline=True),
    ], className='h-50 pt-2 pb-1 px-3'),
    html.Div([
        html.Div([
            dbc.Card([
                dbc.CardHeader([
                    html.H4('Resumen por día', className='text-style m-0'),
                ], className='', id='calendar-heatmap-header'),
                dbc.CardBody([
                    dcc.Graph(
                        id="calendar-heatmap",
                        figure=dict(
                            layout=dict(
                                plot_bgcolor=colors["graph-bg"],
                                paper_bgcolor=colors["graph-bg"],
                            )
                        ),
                        style={"height": "100%"},
                    ),
                ], className='h-100')
            ], className='h-100', outline=True),
        ], className='col-6'),
        html.Div([
            dbc.Card([
                dbc.CardHeader([html.H5('Información general',
                                        className='text-style')],
                               className='px-2 pt-1 p-0'),
                dbc.CardBody([
                    html.Div([
                        dbc.Card([
                            hdlr.chm_card_content(1)
                        ], id='chm_info_card1',
                            className='ml-4 col-3 bg-secondary text-center'),
                        html.Div(className='col-1'),
                        dbc.Card([
                            hdlr.chm_card_content(2)
                        ], id='chm_info_card2',
                            className='h-100 col-3 bg-secondary text-center'),
                        html.Div(className='col-1'),
                        dbc.Card([
                            hdlr.chm_card_content(3)
                        ], id='chm_info_card3',
                            className='h-100 col-3 bg-secondary text-center'),
                    ], className='row h-100 py-4')
                ], className='h-100 w-100 py-1')
            ], className='h-100 w-100')
        ], className='col-6 h-100')
    ], className='h-50 row m-0 pt-2 pb-2')
], className='h-100 w-100')


##############################################################################
#                           ROOT CAUSE LAYOUT                                #
##############################################################################

root_layout = html.Div([
    dbc.Tabs([
        dbc.Tab(label='S1', tab_id='S1'),
        dbc.Tab(label='S2', tab_id='S2'),
        dbc.Tab(label='S3', tab_id='S3'),
        dbc.Tab(label='S4', tab_id='S4'),
        dbc.Tab(label='S5', tab_id='S5'),
        dbc.Tab(label='S6a', tab_id='S6a'),
        dbc.Tab(label='S6b', tab_id='S6b'),
        dbc.Tab(label='S6c', tab_id='S6c'),
        dbc.Tab(label='S7a', tab_id='S7a'),
        dbc.Tab(label='S7b', tab_id='S7b'),
        dbc.Tab(label='S7c', tab_id='S7c')
    ], id='root-tabs', active_tab='S1'),
    html.Div([
        html.Div([
            html.Div([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4('Informacón de la barra', className=
                                'text-style m-0'),
                    ], className='', id='info-header'),
                    dbc.CardBody([
                        html.P("", className='card-text text-left pt-3',
                               id='signal-info'),
                    ], className='h-100')
                ], className='h-100', outline=True)
            ], className = 'h-50 pb-1'),
            html.Div([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4('Selector de señal', className='text-style m-0'),
                    ], className='', id='selector-header'),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id="signal-dropdown",
                            options=[{'label': x, 'value': x} for x in
                                     params['columns']],
                            # options=[{'label': 'x', 'value': 'x'}],
                            value=params['columns'][0],
                            style={
                                'color': colors['text-dropdown'],
                            },
                        ),
                    ], className='h-100')
                ], className='h-100', outline=True)
            ], className='h-50 pt-1')
        ], className='col-3 py-2 pr-1 pl-2'),
        html.Div([
            html.Div([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4('Histograma', className='text-style m-0'),
                    ], className='', id='hist-header'),
                    dbc.CardBody([
                        dcc.Graph(
                            id="hist-plot",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=colors["graph-bg"],
                                    paper_bgcolor=colors["graph-bg"],
                                )
                            ),
                            style={"height": "100%"},
                        ),
                    ], className='h-100')
                ], className='h-100', outline=True),
            ], className='h-50 pb-1'),
            html.Div([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4('Señal sobre tiempo', className='text-style m-0'),
                    ], className='', id='signal-plot-header'),
                    dbc.CardBody([
                        dcc.Graph(
                            id="signal-plot",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=colors["graph-bg"],
                                    paper_bgcolor=colors["graph-bg"],
                                )
                            ),
                            style={"height": "100%"},
                        ),
                    ], className='h-100')
                ], className='h-100', outline=True),
            ], className='h-50 pt-1')
        ], className='col-9 py-2 pr-2 pl-1'),
    ], className='row m-0', style={"height": "calc(100% - 40px)"})
], className='h-100')


