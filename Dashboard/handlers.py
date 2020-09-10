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
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
import pickle
from datetime import date, timedelta, datetime

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
        data_len = len(data['general']),
        columns = data['S1'].columns,
        family_font='Arial, sans-serif',  # Graph Text Font
        size_font=16,  # Graph Text Size
        size_font_cards=22,  # Graph Text Size
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
            'graph-bg2': '#4d4d4d'
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
def get_plant_plot(idx):
    if idx < 100:
        idx1 = 0
    else:
        idx1 = idx-100
    df = pd.DataFrame(data['general'])
    df = df.loc[idx1:idx + 100, :]
    column = 'label_global'
    datemin1 = df['timestamp_barra'].min() - timedelta(hours=0.5)
    datemax1 = df['timestamp_barra'].max() + timedelta(hours=0.5)


    # Scatter plot con del label de comportamiento de la planta
    trace = dict(
        type="scatter",
        ids=list(df.index),
        x=df['timestamp_barra'],
        y=df[column],
        line={"color": "dimgray"},
        hoverinfo='x+text',
        # Texto que se muestra al pasar el cursor por encima de un punto
        hovertext = ['<b>Id</b>: {}<br>'.format(index) +
                     '<b>All</b>: {}<br>'.format(row[column]) +
                     '<b>S1</b>: {}<br>'.format(row['label_S1']) +
                     '<b>S2</b>: {}<br>'.format(row['label_S2']) +
                     '<b>S3</b>: {}<br>'.format(row['label_S3']) +
                     '<b>S4</b>: {}<br>'.format(row['label_S4']) +
                     '<b>S5</b>: {}<br>'.format(row['label_S5']) +
                     '<b>S6a</b>: {}<br>'.format(row['label_S6a']) +
                     '<b>S6b</b>: {}<br>'.format(row['label_S6b']) +
                     '<b>S6c</b>: {}<br>'.format(row['label_S6c']) +
                     '<b>S7a</b>: {}<br>'.format(row['label_S7a']) +
                     '<b>S7b</b>: {}<br>'.format(row['label_S7b']) +
                     '<b>S7c</b>: {}<br>'.format(row['label_S7c']) 
                     for index, row in df.iterrows()],
        mode="markers",
        name='Label',
        marker=dict(
            color=[colors['plantplot-mk-green'] if x > 15 else
                   colors['plantplot-mk-red'] for x in df[column]],
            # size=10,
        ),
    )
    
    # Opciones de estilo del gráfico
    layout = dict(
        plot_bgcolor=colors["graph-bg"],
        paper_bgcolor=colors["graph-bg"],
        font={"color": colors['text'], "size": params['size_font'], "family":
              params['family_font']},
        margin={"t": 30, "b": 50, "r": 15, "l": 15},
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
                22.5
            ],
            "tickvals": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22],
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
                y0=16, 
                y1=22.5, 
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
                y1=16, 
                fillcolor=colors['plantplot-bg-red'], 
                layer='below',
                linewidth=0,
            ),
            # Linea de color rojo para estilizar el scatter
            dict(
                type="line",
                x0=datemin1,
                y0=16,
                x1=datemax1,
                y1=16,
                line=dict(
                    color=colors['plantplot-l-red'],
                    width=4,
                ),
                layer='below'
            )
        ],
    )
    return trace, layout

# Calendar HeatMap  Figure Layout and Traces
def calendar_heatmap(seccion):
    df = data['general']
    if seccion == 'global':
        label_max = 22
    else:
        label_max = 2

    df['day'] = [datetime.date(fecha) for fecha in df['timestamp_barra']]

    d1 = datetime.date(df['timestamp_barra'].min())
    d2 = datetime.date(df['timestamp_barra'].max())
    delta = d2 - d1
    num_months = (d2.year - d1.year) * 12 + (d2.month - d1.month)
    date_list = [d2 - timedelta(days=x) for x in range(delta.days)]
    days_df = pd.DataFrame(index=date_list)
    days_df['labels'] = df.groupby('day').mean()['label_' + seccion]
    days_df = days_df.fillna(-1)

    dates_in_year = [d1 + timedelta(i) for i in range(delta.days+1)] #gives me a list with datetimes for each day a year
    weekdays_in_year = [i.weekday() for i in dates_in_year] #gives [0,1,2,3,4,5,6,0,1,2,3,4,5,6,…] (ticktext in xaxis dict translates this to weekdays
    weeknumber_of_dates = [i.strftime("%Gww%V") for i in dates_in_year] #gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,…] name is self-explanatory
    z = np.array([-1 if x<0 else 0 if x<label_max*0.85 else 1 
                  if x<label_max*0.95 else 2 for x in days_df['labels'].values]) #df.groupby('day').mean()[f'label{label}'] 
    text = [str(i) for i in dates_in_year] #gives something like list of strings like '2018-01-25' for each date. Used in data trace to _ta good hovertext.

    xtickvals = [d1.strftime("%Gww%V")]
    xticktext = [d1.strftime("%b")]
    month = d1.month + 1
    year = d1.year
    for i in range(1, num_months):
        if month > 12:
            month = 1
            year += 1
        fecha = datetime(year, month, 1)
        xtickvals = np.append(xtickvals, fecha.strftime("%Gww%V"))
        xticktext = np.append(xticktext, fecha.strftime("%b"))
        month += 1

    trace = dict(
        type='heatmap',
        x=weeknumber_of_dates,
        y=weekdays_in_year,
        z=z,
        text=text,
        hoverinfo="text+z",
        xgap=3,  # this
        ygap=3,  # and this is used to make the grid-like apperance
        zmin=-1,
        zmax=2,
        showscale=True,
        colorscale=[(0, colors['graph-bg2']),   (0.25, colors['graph-bg2']),
                    (0.25, colors['chm-fail']),   (0.5, colors['chm-fail']),
                    (0.5, colors['chm-dev']), (0.75, colors['chm-dev']),
                    (0.75, colors['chm-good']),  (1.00, colors['chm-good'])],
        colorbar=dict(
            title="Anomalías",
            # titleside="top",
            tickmode="array",
            tickvals=[-0.65, 0.1, 0.85, 1.66],
            ticktext=["Sin produccion", "Muchas", "Algunas", "Pocas"],
            ticks="outside"
        ),
    )
    layout = dict(
        yaxis=dict(
            showline=False, showgrid=False, zeroline=False, tickmode="array",
            ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            tickvals=[0, 1, 2, 3, 4, 5, 6], ticks='',
        ),
        xaxis=dict(
            showline=False, showgrid=False, zeroline=False, ticktext=xticktext,
            tickvals=xtickvals,
        ),
        font={"color": colors['text'], "size": params['size_font'],
              "family": params['family_font']},
        plot_bgcolor=colors["graph-bg"],
        paper_bgcolor=colors["graph-bg"],
        margin=dict(t=40, b=40, r=40, l=40),
    )
    return dict(data=[trace], layout=layout)

# Función que devuelve los traces y layout del histograma
def histogram(seccion, column, id_data):
    if id_data is None:
        id_data = 0
    if id_data < 100:
        idx1 = 0
    else:
        idx1 = id_data - 100
    df = data[seccion]
    df = df.loc[idx1:id_data + 100, :]
    # Datos historicos del histograma S1
    df_hist = data[seccion]
    trace = dict(
        type="histogram",
        name='Historico',
        x=df_hist[column],
        nbins=10,
        bingroup=1,
        histnorm='percent',
        label='historical',
        marker={
            'line': {
                'width': 1,
                'color': colors['histogram-hist-br'],
            },
            'color': colors['histogram-hist'],
        },
    )

    # Datos seleccionados con la id para el histograma S1
    trace2 = dict(
        type="histogram",
        name='Datos cercanos',
        x=df[column],
        bingroup=1,
        nbins=10,
        histnorm='percent',
        opacity=0.75,
        label='current',
        marker={
            'line': {
                'width': 1,
                'color': colors['histogram-act-br'],
            },
            'color': colors['histogram-act'],
        },
    )
    # Layout del histograma S1
    layout = dict(
        barmode='overlay',
        plot_bgcolor=colors["graph-bg"],
        paper_bgcolor=colors["graph-bg"],
        font={"color": colors['text'], "size": params['size_font'],
              "family": params['family_font']},
        margin={'t': 25, 'b': 45, 'l': 30, 'r': 15},
        legend={
            "orientation": "h",
            "xanchor": "center",
            "yanchor": "top",
            "y": 1.3,  # play with it
            "x": 0.2  # play with it
        },
        yaxis={
            "gridcolor": colors["grid"],
        },
        shapes=[
            {
                'type': "line",
                # 'xref':df[df['id']==id_data['id']][column].iloc[0],
                'yref': 'paper',
                'x0': df.loc[id_data, :][column],
                'y0': 0,
                'x1': df.loc[id_data, :][column],
                'y1': 0.95,
                'line': dict(
                    color=colors['plantplot-l-red'],
                    width=4,
                ),
            },
        ],
    )
    return dict(data=[trace, trace2], layout=layout)

# Función que devuelve el trace y layout del gráfico de la señal
def signal_plot(seccion, column, id_data):
    if id_data is None:
        id_data = 0
    if id_data < 100:
        idx1 = 0
    else:
        idx1 = id_data - 100
    
    df = data[seccion]
    df1 = df.loc[idx1:id_data + 100, :]
    df2 = data['general']
    df2 = df2.loc[idx1:id_data + 100, :]
    mean = df[column].mean()
    std = 2*df[column].std()
    
    # Signal Plot S1
    trace = dict(
        type="scatter",
        y=df1[column],
        x=df2['timestamp_barra'],
        line={"color": colors['signal-line']},
        mode="lines",
        name='Señal',
    )

    trace2 = dict(
        type="scatter",
        y=df1.loc[id_data, :][column],
        x=df2.loc[id_data, :]['timestamp_barra'],
        line={"color": colors['signal-marker']},
        mode="markers",
        marker=dict(symbol='cross', size=12),
        name='Seleccionado',
    )

    # Signal Layout S1
    layout = dict(
        plot_bgcolor=colors["graph-bg"],
        paper_bgcolor=colors["graph-bg"],
        font={"color": colors['text'], "size": params['size_font'],
              "family": params['family_font']},
        margin={'t': 25, 'b': 45, 'l': 30, 'r': 15},
        legend={
            "orientation": "h",
            "xanchor": "center",
            "yanchor": "top",
            "y": 1.3,  # play with it
            "x": 0.2  # play with ii
        },
        xaxis={
            "showline": True,
            "zeroline": False,
            "fixedrange": False,
            "ylabel": column,
        },
        yaxis={
            "range": [
                df[column].min() - 0.1*(df[column].max() - df[column].min()),
                df[column].max() + 0.1*(df[column].max() - df[column].min()),
            ],
            "showgrid": True,
            "showline": True,
            "zeroline": False,
            "gridcolor": colors["grid"],
            "nticks": 10
        },
        shapes=[
            {
                'type': "line",
                # 'xref':df[df['id']==id_data['id']][column].iloc[0],
                'xref': 'paper',
                'x0': 0,
                'y0': mean - std,
                'x1': 1,
                'y1': mean - std,
                'line': dict(
                    color=colors['plantplot-l-red'],
                    width=4,
                    dash="dashdot",
                ),
            },
            {
                'type': "line",
                # 'xref':df[df['id']==id_data['id']][column].iloc[0],
                'xref': 'paper',
                'x0': 0,
                'y0': mean + std,
                'x1': 1,
                'y1': mean + std,
                'line': dict(
                    color=colors['plantplot-l-red'],
                    width=4,
                    dash="dashdot",
                ),
            },
        ],
    )
    return dict(data=[trace, trace2], layout=layout)

# Card content
def chm_card_content(card):
    data={
        1: {
            "first": '% de efciencia en los últimos 30 días',
            "second": '97%',
            "third": '30 Mayo 2017 - 30 Junio 2017'
        },
        2: {
            "first": 'Racha actual de eficiencia',
            "second": '3 días',
            "third": '27 Junio 2017 - 30 Junio 2017'
        },
        3: {
            "first": 'Mayor racha de eficiencia',
            "second": '27 días',
            "third": '3 Mayo 2017 - 30 Mayo 2017'
        },
    }
    return html.Div([
        html.Div(data[card]['first'], style={"font-size": "1rem", "color":
                                             colors['text']}),
        html.Div(data[card]['second'], style={"font-size": "3rem"}),
        html.Div(data[card]['third'], style={"font-size": "1rem", "color":
                                             colors['text']}),
    ], className='my-auto')

def dropdown_options(seccion):
    columns = data[seccion].columns
    options = [{'label': x, 'value': x} for x in columns]
    value = columns[0]
    return options, value

# Función que devuelve el texto que ira dentro del recuadro de información de la barra seleccionada page-2
def text_info(seccion, column, id_data):
    if id_data is None:
        id_data = 0
    date = data['general'].loc[id_data, 'timestamp_barra']
    value = data[seccion].loc[id_data, column]
    mean = data[seccion].mean()
    mean = mean[column]
    std = 2*data[seccion].std()
    std = std[column]
    spaces = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
    text = dcc.Markdown('''**ID**: {}  
                        **Fecha**: {}  
                        **{}**: {:.2f}  
                        **Media**: {:.2f}  
                        **Desviación estandard**: {:.2f}'''.format(
        id_data, date, column, value, mean, std),
        style={"color": colors['text'],
               "font-size": params['size_font_cards'],
               "font-family": params['family_font']})       
    return text