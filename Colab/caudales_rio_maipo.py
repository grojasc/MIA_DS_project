# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 22:46:02 2022

@author: nicos
"""
import os
import pandas as pd
import geopandas as gpd
from datetime import datetime
from tqdm import tqdm
# %%

caudales = pd.read_csv(os.path.join(
        'datos hidricos',  'cr2_qflxDaily_2018.txt'), sep=",", decimal=".")

info_estaciones = caudales.head(14).T.reset_index()
info_estaciones.columns = info_estaciones.iloc[0, :]
info_estaciones = info_estaciones.iloc[1:, :]

info_rio_maipo = info_estaciones.loc[
        info_estaciones.nombre_cuenca == 'Rio Maipo'].sort_values(
        'latitud', ignore_index=True)

for col in ['inicio_observaciones',
       'fin_observaciones']:
    info_rio_maipo[col]= info_rio_maipo[col].apply(lambda x:
        datetime.strptime(x, '%Y-%m-%d').date())

estaciones_rio_maipo = ['codigo_estacion']
estaciones_rio_maipo.extend(list(info_rio_maipo.codigo_estacion))
caudales_rio_maipo = caudales[estaciones_rio_maipo]
caudales_rio_maipo = caudales_rio_maipo.iloc[14:, :]

# %%
caudales_rio_maipo.rename(columns={'codigo_estacion':'dia'}, inplace=True)
caudales_rio_maipo['dia'] = caudales_rio_maipo['dia'].apply(lambda x:
        datetime.strptime(x, '%Y-%m-%d').date())

info_rio_maipo.set_index('codigo_estacion', inplace=True)
database_rio_maipo = pd.DataFrame()
    
for estacion in tqdm(estaciones_rio_maipo[1:]):
    caudal_estacion = caudales_rio_maipo[['dia', estacion]]
    caudal_estacion = caudal_estacion.loc[
            caudal_estacion.dia>info_rio_maipo.loc[estacion, 'inicio_observaciones']]
    caudal_estacion.columns = ['dia', 'caudal']
    caudal_estacion['estacion'] = estacion
    database_rio_maipo = database_rio_maipo.append(caudal_estacion)

# %% plots estaciones
    
info_estaciones = gpd.GeoDataFrame(
        info_estaciones, geometry=gpd.points_from_xy(
                info_estaciones.longitud, info_estaciones.latitud))

