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

params = hdlr.get_params(hdlr.dark)

colors = params['colors']


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
                )
            ], className='h-100')
        ], className='h-100', outline=True),
    ], className='h-50 pt-2 pb-1 px-3'),
    html.Div([
        html.Div([
            dbc.Card([
                dbc.CardHeader([
                    html.H4('Resumen por día', className='text-style m-0'),
                ], className='', id='calendar-heatmap'),
                dbc.CardBody([
                    
                ], className='h-100')
            ], className='h-100', outline=True),
        ], className='col-6'),
        html.Div([
            dbc.Card([
                dbc.CardHeader([
                    html.H4('Informacion general', className='text-style m-0'),
                ], className='', id='info-cards'),
                dbc.CardBody([
                    
                ], className='h-100')
            ], className='h-100', outline=True),
        ], className='col-6')
    ], className='h-50 row m-0 pt-1 pb-2')
], className='h-100 w-100')


##############################################################################
#                              KPIs LAYOUT                                   #
##############################################################################

kpis_layout = html.Div([
], className='h-100')


##############################################################################
#                             CAETAS LAYOUT                                  #
##############################################################################

casetas_layout = html.Div([
], className='h-100')
