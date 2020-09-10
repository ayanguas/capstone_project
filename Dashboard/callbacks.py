# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 11:30:10 2020

@author: Albert Yanguas - ayanguasrovira@gmail.com
"""

from dash.dependencies import Input, Output, State
from dash import callback_context

from app import app

import handlers as hdlr

@app.callback(Output('store-id', 'data'),
              [Input('plant-plot', 'clickData')])
def change_iddata(click_data):
    if click_data is not None:
        point_id = -1
        if 'points' in click_data.keys():
            if 'id' in click_data['points'][0].keys():
                point_id = click_data['points'][0]['id']
                print(point_id)
        return point_id

@app.callback(Output('url', 'pathname'),
              [Input('plant-plot', 'clickData')])
def change_page(click_data):
    if click_data is not None:
        return '/root'
    else:
        return '/home'

# Plant plot callback
@app.callback(
    Output("plant-plot", "figure"),
    [Input("signal-update", "n_intervals")])
def display_plantplot(idx):
    """Return plant plot traces and layout"""
    trace, layout = hdlr.get_plant_plot(idx)
    return dict(data=[trace], layout=layout)

# Calendar Heatmap callback
@app.callback(
    Output("calendar-heatmap", "figure"),
    [Input("signal-update", "n_intervals")])
def display_chmap(idx):
    """Return calendar heatmap figure"""
    return hdlr.calendar_heatmap('global')

# Signal dropdown callback
@app.callback(
    [Output("signal-dropdown", "options"), Output("signal-dropdown", "value")],
    [Input("root-tabs", "active_tab")])
def dropdown_options(seccion):
    """Update dropdown values"""
    return hdlr.dropdown_options(seccion)

# Histogram callback
@app.callback(
    Output("hist-plot", "figure"),
    [Input("url", "pathname"), Input("signal-dropdown", "value")],
    [State("root-tabs", "active_tab"), State('store-id', 'data')])
def display_hist(url, column, seccion, id_data):
    """Return kpi1_plot traces and layout"""
    return hdlr.histogram(seccion, column, id_data)
    
# Signal plot callback
@app.callback(
    Output("signal-plot", "figure"),
    [Input("url", "pathname"), Input("signal-dropdown", "value")],
    [State("root-tabs", "active_tab"), State('store-id', 'data')])
def display_signal(url, column, seccion, id_data):
    """Return kpi1_plot traces and layout"""
    return hdlr.signal_plot(seccion, column, id_data)

# Signal plot callback
@app.callback(
    Output("signal-info", "children"),
    [Input("signal-dropdown", "value")],
    [State("root-tabs", "active_tab"), State('store-id', 'data')])
def display_info(column, seccion, id_data):
    """Return kpi1_plot traces and layout"""
    return hdlr.text_info(seccion, column, id_data)