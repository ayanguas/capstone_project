# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 11:59:05 2020

@author: Albert Yanguas - ayanguasrovira@gmail.com
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import plotly.graph_objs as go

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import pickle

dark = True

data = pickle.load(open('../data/dashboard_data.pickle', 'rb'))

def get_params(dark):
    """Return app parameters"""
    font_awesome2 = ["//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/" +
                     "font-awesome.css"]

    if dark:
        graph_bg = '#303030'  # 272B30'
        text_color = '#AAAA9F'
        text_highlight = '#CCCCC0'
        pp_bg_green = '#356437'
        pp_bg_red = '#653434'
        pp_mk_green = '#59C159'
        pp_mk_red = '#EC5550'
        pp_ma_grey = '#AAAAAA'
        chm_good = '#DDDDDD'
        chm_dev = '#e8b68b'
        chm_fail = '#e04f38'
        secondary = '#686868'
        polar_fill = 'rgba(230, 181, 76, 0.75)'
        external_stylesheets = [dbc.themes.DARKLY, font_awesome2]
        navbar_image = "logo-ub-navabr.png"
    else:
        graph_bg = ''
        text_color = '262626'
        text_highlight = '0d0d0d'
        pp_bg_green = '#F7FAF0'
        pp_bg_red = '#F9E9E0'
        pp_mk_green = '#76B7B2'
        pp_mk_red = '#E15759'
        pp_ma_grey = '#DDDDDD'
        chm_green = '#EEEEEE'
        chm_dev = '#E8C2A0'
        chm_fail = '#E06E5D'
        secondary = ''
        polar_fill = ''
        external_stylesheets = [dbc.themes.BOOTSTRAP, font_awesome2]
        navbar_image = "logo-ub-navabr.png"

    params = dict(
        family_font='Arial, sans-serif',  # Graph Text Font
        size_font=16,  # Graph Text Size
        navbar_image=navbar_image,
        external_stylesheets=external_stylesheets,
        navbar_logo_size="90%",  # Navbar logo size
        external_scripts=[{
            'src': 'https://kit.fontawesome.com/c67d65477e.js',
            'crossorigin': 'anonymous'
        }],
        colors={
            'navbar': 'secondary',
            'title-bg': '#444444',
            'graph-bg': graph_bg,
            'text': text_color,
            'text-highlight': text_highlight,
            'text-dropdown': '#3A3A3A',
            'plantplot-bg-green': pp_bg_green,  # Plantplot Background Green
            'plantplot-bg-red': pp_bg_red,  # Plantplot Background Red
            'plantplot-l-red': '#B31919',  # Plantplot Line Red #E46B6B
            'plantplot-mk-green': pp_mk_green,  # Plantplot Marker Green
            'plantplot-mk-red': pp_mk_red,  # Plantplot Merker Red
            'plantplot-ma-grey': pp_ma_grey,  # Plantplot Moving Average
                                              # line grey
            'chm-good': chm_good,  # Calendar HeatMap Green
            'chm-dev': chm_dev,  # Calendar HeatMap Yellow
            'chm-fail': chm_fail,  # Calendar HeatMap Red
            'histogram-act': '#FFA64D',  # Histogram Actual
            'histogram-act-br': '#FF8C1A',  # Histogram Actual Border
            'histogram-hist': '#4DA6FF',  # Histogram Historical
            'histogram-hist-br': '#1A8CFF',  # Histogram Historical Border
            'grid': '#636363',
            'signal-line': '#FEC036',  # Linea amarilla del gráfico de la señal
            'signal-marker': '#B31919',
            'stacked-bar-yellow': '#FEC036',
            'secondary': secondary,  # Color gris de los titulos de las Cards
            'polar-fill': polar_fill,  # Color amarillo de relleno
            'green-on': 'rgba(51, 165, 50, 1)',
            'yellow-on': 'rgba(250, 210, 1, 1)',
            'red-on': 'rgba(251, 18, 47, 1)',
            'green-off': 'rgba(51, 165, 50, 0.3)',
            'yellow-off': 'rgba(250, 210, 1, 0.3)',
            'red-off': 'rgba(251, 18, 47, 0.3)',
        }
    )
    return params


params = get_params(dark)

colors = params['colors']

graph_layout = dict(plot_bgcolor=colors["graph-bg"],
                    polar_bgcolor=colors["secondary"],
                    paper_bgcolor=colors["graph-bg"],
                    font={"color": colors['text'], "size": params['size_font'],
                          "family": params['family_font']},
                    margin=dict(t=40, b=40, r=40, l=40))


# Función que devuelve el trace y layout de plant-plot
def get_plant_plot():
    
    df = pd.DataFrame(data['general'])
    column = 'label'
    datemin1 = df['date'].min() - timedelta(hours=2)
    datemax1 = df['date'].max() + timedelta(hours=2)
    
    moving_average = df[column].rolling(3).mean()
    
    # Scatter plot con del label de comportamiento de la planta
    trace = dict(
        type="scatter",
        ids=df['id'],
        x=df['date'],
        y=df[column],
        line={"color": "dimgray"},
        hoverinfo='x+text',
        # # Texto que se muestra al pasar el cursor por encima de un punto
        hovertext = ['<b>Id</b>: {}<br><b>All</b>: {}<br><b>S1</b>: {}<br><b>S2</b>: {}<br><b>S3</b>: {}'.format(row['id'],row['label'], row['label_S1'], row['label_S2'], row['label_S3']) \
                      for index, row in df.iterrows()],
        mode="markers",
        name='Label',
        marker=dict(
            color=[colors['plantplot-mk-green'] if x > 3 else colors['plantplot-mk-red'] for x in df['label']],
            # size=10,
        ),
    )
        
    trace2 = dict(
        type="scatter",
        x=df['date'],
        y=moving_average,
        line={"color": colors['plantplot-ma-grey']},
        mode="line",
        name='Moving average 5',
    )
        
    # Opciones de estilo del gráfico
    layout = dict(
        plot_bgcolor=colors["graph-bg"],
        paper_bgcolor=colors["graph-bg"],
        font={"color": colors['text'], "size": size_font, "family": family_font,},
        margin={"t":30, "b": 50, "r": 15, "l":15},
        # height=500,
        xaxis={
            "range": [datemin1, datemax1],
            "showline": False,
            "zeroline": False,
            "fixedrange": True,
            "ylabel": column,
        },
        yaxis={
            "range": [
                0,
                6.5
            ],
            "tickvals": [2,4,6],
            "showgrid": False,
            "showline": False,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": colors["grid"],
            "nticks": 7,
            "automargin": True,
        },
        shapes=[
            # Rectangulo de color verde para estilizar el scatter
            dict(
                type='rect', 
                x0=datemin1, 
                x1=datemax1, 
                y0=4, 
                y1=6.5, 
                fillcolor=colors['plantplot-bg-green'], 
                layer='below',
                linewidth=0,
            ),
            # Rectangulo de color rojo para estilizar el scatter
            dict(
                type='rect', 
                x0=datemin1, 
                x1=datemax1, 
                y0=0, 
                y1=4, 
                fillcolor=colors['plantplot-bg-red'], 
                layer='below',
                linewidth=0,
            ),
            # Linea de color rojo para estilizar el scatter
            dict(
                type="line",
                x0=datemin1,
                y0=4,
                x1=datemax1,
                y1=4,
                line=dict(
                    color=colors['plantplot-l-red'],
                    width=4,
            
                ),
                layer='below'
            )
        ],
    )
    return trace, trace2, layout