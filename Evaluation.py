# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 16:38:02 2020

@author: Albert Yanguas - ayanguasrovira@gmail.com
"""
import pandas as pd
import numpy as np
import pickle

def save_pickle(data, file_name):
    with open(file_name + '.pickle', 'wb') as f:
        pickle.dump(data, f)

data = pickle.load(open('data/datos_capstone_project.pickle',
                        'rb'))
scalers = pickle.load(open('data/scalers.pickle',
                           'rb'))
pcas = pickle.load(open('data/pcas.pickle',
                        'rb'))
thresholds = pickle.load(open('data/thresholds.pickle',
                              'rb'))
models = pickle.load(open('data/models.pickle',
                          'rb'))


seccions = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6a', 'S6b', 'S6c', 'S7a', 'S7b',
            'S7c']

for seccion in seccions:
    df = pd.DataFrame(data[seccion])
    df.dropna(axis=0, inplace=True)

    scaler = scalers[seccion]
    df_norm = scaler.transform(df)

    pca = pcas[seccion]
    pc = pca.transform(df_norm)

    model = models[seccion]
    threshold = thresholds[seccion]
    y = model.decision_function(pc)

    normalidad = np.zeros(len(y))
    normalidad[y >= threshold[1]] = 1
    normalidad[y >= threshold[0]] = 2

    data['general'].loc[df.index, 'label_' + seccion] = normalidad

    pnormal = (normalidad[normalidad == 2].size/normalidad.size)*100
    pdesviacion = (normalidad[normalidad == 1].size/normalidad.size)*100
    panomalo = (normalidad[normalidad == 0].size/normalidad.size)*100

    print(seccion + ':')
    print("Normalidad: %0.1f; Desviación: %0.1f; Anomalia: %0.1f" %
          (pnormal, pdesviacion, panomalo))

data['general'] = data['general'].drop('timestamp_millis', axis=1)
data['general'] = data['general'].dropna(axis=0)

for seccion in seccions:
    data[seccion] = data[seccion].iloc[data['general'].index, :]
    data[seccion] = data[seccion].reset_index(drop=True)

data['general'] = data['general'].reset_index(drop=True)

filter_col = [col for col in data['general'] if col.startswith('label_')]

data['general']['label_global'] = data['general'
                                       ].loc[:, filter_col].sum(axis=1)

save_pickle(data, 'data/dashboard_data')
