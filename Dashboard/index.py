# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 11:31:16 2020

@author: Albert Yanguas - ayanguasrovira@gmail.com
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import callback_context
import dash_bootstrap_components as dbc

from app import app, server
from layouts import home_layout, root_layout, navbar
import callbacks
# from handlers import get_params, dark

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='store-id'),
    navbar,
    html.Div(id='page-content', className='w-100', style={"height": '92vh'}),
    html.Footer([
        html.Div([
            'Capstone Project'
        ], className='text-center')
    ], className='py-1', style={"height": '3vh'}),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """Return page layouts."""
    if pathname == '/root':
        return root_layout
    else:
        return home_layout

if __name__ == '__main__':
    app.run_server(debug=True)
