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

from app import app
from layouts import home_layout, kpis_layout, casetas_layout
import callbacks
from handlers import get_params, dark

params = get_params(dark)

colors = params['colors']

# Barra de navegacion de la aplicacion
navbar = dbc.Navbar([
    html.A(
        # Imagen con el logo de Dattium que nos llevara a la página
        # principal de la App
        html.Img(src=app.get_asset_url(params['navbar_image']),\
                                  height=params['navbar_logo_size']),
        href="/home",
        className='float-right col-2 h-100'
    ),
    dbc.Nav([
        dbc.NavItem(dbc.NavLink("Home", href="/home",
                                style={"color": colors['text']})),
        dbc.NavItem(dbc.NavLink("KPIs", href="/kpis",
                                style={"color": colors['text']},
                                id='report_page_nav')),
        dbc.NavItem(dbc.NavLink("Casetas", href="/casetas",
                                style={"color": colors['text']},
                                id='comparativas_page_nav')),
    ], className=''),
], className='lg py-1 px-1', color=colors['navbar'], style={"height": '5vh'})

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
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
    if pathname == '/kpis':
        return kpis_layout
    elif pathname == '/casetas':
        return casetas_layout
    # elif pathname == '/kpis':
    #     return kpis_layout
    else:
        return home_layout


if __name__ == '__main__':
    app.run_server(debug=True)
