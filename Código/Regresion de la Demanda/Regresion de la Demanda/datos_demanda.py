# -*- coding: utf-8 -*-
"""
Created on Tue May 17 23:47:27 2022

@author: Dinde
"""

import pandas as pd
from scipy.interpolate import interp1d
import numpy as np

#------------- y_demanda ---------------------
y_prediccion = pd.read_excel('y_demanda_datos/Demanda agua potable.xlsx', index_col='Año' )['Consumo agua potable (Aguas Andinas) miles de m3']
y_prediccion = y_prediccion.rename('Demanda Anual de Agua').iloc[2:14]
y_prediccion.index = y_prediccion.index.astype(int)
#--------------------------------------------- 

#-------------- Poblacion RM ------------------
pob_ano = pd.read_csv('y_demanda_datos/poblacion_region.txt', index_col='periodo')
pob_ano = pob_ano[pob_ano['region'] == 13]
# pob_ano = pob_ano.iloc[7:-10]['poblacion'].rename('Poblacion')
pob_ano = pob_ano['poblacion'].rename('Poblacion')


#-------------- Ruralidad -----------------
por_ruralidad = pd.read_excel('y_demanda_datos/Indice ruralidad .xlsx').T
por_ruralidad.columns = por_ruralidad.iloc[0,:]
por_ruralidad = por_ruralidad.iloc[1:]
por_ruralidad = por_ruralidad['porcentaje_rural'].rename('por_poblacion_rural').astype(float)#.iloc[7:7+12]

#------------- Tasa de pobreza -------------------
tasa_pobreza = pd.read_excel('y_demanda_datos/Tasa de pobreza.xlsx').T
tasa_pobreza.columns = tasa_pobreza.iloc[0,:]
tasa_pobreza = tasa_pobreza.squeeze()[1:].rename('Tasa de pobreza').astype(float)
# tasa_pobreza = tasa_pobreza.iloc[4:-10].squeeze().rename('Tasa de pobreza')

#-------------- Precio Cobre ------------------
precio_cobre = pd.read_excel('y_demanda_datos/Precio cobre.xlsx', index_col=('Ano')).squeeze().rename('Precio Cobre Promedio Anual USD')
# precio_cobre = pd.read_excel('y_demanda_datos/Precio cobre.xlsx', index_col=('Ano')).iloc[:-2].squeeze().rename('Precio Cobre Promedio Anual USD')


#-------------- Demanda eléctrica generacion -------------
generacion_electrica = pd.read_excel('y_demanda_datos/Generacion electrica.xlsx', index_col='YEAR').iloc[:,:-2]
# generacion_electrica = pd.read_excel('y_demanda_datos/Generacion electrica.xlsx', index_col='YEAR').iloc[2:-1,:-2]
generacion_electrica.columns = ['Demanda Hidráulica Embalse','Demanda Hidráulica Pasada']

#-------------- Pib per capita / variacion anual -----------------------
pib_per_capita = pd.read_excel('y_demanda_datos/Pib per capita.xlsx').sort_values('ano').reset_index(drop=True)
pib_per_capita.index = pib_per_capita['ano']
pib_per_capita = pib_per_capita.drop(columns='ano')[:-1]

#-------------- Crecimiento Mundial ------------------
crecimiento_mundial = pd.read_excel('y_demanda_datos/Crecimiento Poblacion Mundial.xlsx', index_col='Año')

#--------------- Precio del petróleo -------------------
precio_petroleo = pd.read_excel('y_demanda_datos/Petroleo.xlsx')
precio_petroleo.index = precio_petroleo['Periodo']
precio_petroleo = precio_petroleo.groupby([pd.Grouper(freq='Y') ]).mean()
precio_petroleo.index = pd.DatetimeIndex(precio_petroleo.index).year
precio_petroleo = precio_petroleo#[:-2]


# -----------------------------------------------------------------------------
#------------------------- Concatenacion total  -------------------------------

dataset_demanda = pd.concat([pob_ano, por_ruralidad, tasa_pobreza, precio_cobre, generacion_electrica, pib_per_capita,\
                            crecimiento_mundial, precio_petroleo, y_prediccion ], axis=1)
dataset_demanda.index = dataset_demanda.index.astype(int)
dataset_demanda = dataset_demanda.loc[2009:]

#------------------------------------------------------------------------------
from sklearn.linear_model import LinearRegression
regres = LinearRegression()

#Poblacion
regres.fit(dataset_demanda.index[dataset_demanda.index < 2031].to_numpy().reshape(-1,1) ,dataset_demanda.loc[:2030,'Poblacion'].to_numpy())
dataset_demanda.loc[2031:,'Poblacion'] = regres.predict(dataset_demanda.index[dataset_demanda.index >= 2031].to_numpy().reshape(-1,1))

#Taza de pobreza
regres.fit(tasa_pobreza.index.to_numpy().reshape(-1,1), tasa_pobreza.to_numpy())
print(regres.predict(np.arange(2031,2036).reshape(-1,1)))
dataset_demanda.loc[2031:,'Tasa de pobreza'] = regres.predict(np.arange(2031,2036).reshape(-1,1))

# print(dataset_demanda['Demanda Hidráulica Embalse'].loc[:2021])
# print(np.arange(2009,2022).reshape(-1,1))
# print(dataset_demanda['Demanda Hidráulica Embalse'][:2021].to_numpy())

# #cobre
# # regres.fit(np.arange(2009,2022).reshape(-1,1), dataset_demanda['Demanda Hidráulica Embalse'].loc[:2021].to_numpy() )
# # dataset_demanda.loc[:,'Demanda Hidráulica Embalse'] = regres.predict( np.arange(2022,2036).reshape(-1,1) )


dataset_demanda.iloc[:,:-1]= dataset_demanda.iloc[:,:-1].interpolate(axis='index', method='linear')
dataset_demanda.to_excel('dataset_demanda.xlsx')












