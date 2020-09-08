# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 11:29:34 2020

@author: Albert Yanguas - ayanguasrovira@gmail.com
"""

import dash
from handlers import get_params, dark

params = get_params(dark)

app = dash.Dash(__name__, suppress_callback_exceptions=True, 
                external_stylesheets=params['external_stylesheets'],
                external_scripts=params['external_scripts'])
server = app.server
