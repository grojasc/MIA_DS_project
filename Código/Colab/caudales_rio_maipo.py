# -*- coding: utf-8 -*-
"""
Este script busca obtener información en formato relacional
de los caudales promedio por día a partir de los datos de caudal del cr2
@author: nicos
"""
import os
import pandas as pd
import geopandas as gpd
from datetime import datetime
from tqdm import tqdm
# %%

caudales = pd.read_csv(os.path.join(
        'Data',  'cr2_qflxDaily_2018.txt'), sep=",", decimal=".",
 low_memory=False)

# Información de estaciones
info_estaciones = caudales.head(14).T.reset_index()
info_estaciones.columns = info_estaciones.iloc[0, :]
info_estaciones = info_estaciones.iloc[1:, :]

# filtramos las estaciones de la cuenca rio maipo
info_rio_maipo = info_estaciones.loc[
        info_estaciones.nombre_cuenca == 'Rio Maipo'].sort_values(
        'latitud', ignore_index=True)

# Las observaciones se llevan a formato date
for col in ['inicio_observaciones',
       'fin_observaciones']:
    info_rio_maipo[col]= info_rio_maipo[col].apply(lambda x:
        datetime.strptime(x, '%Y-%m-%d').date())

estaciones_rio_maipo = ['codigo_estacion']
estaciones_rio_maipo.extend(list(info_rio_maipo.codigo_estacion))
caudales_rio_maipo = caudales[estaciones_rio_maipo]
caudales_rio_maipo = caudales_rio_maipo.iloc[14:, :]

# %%
# Extraemos información del caudal por día según la disponibilidad de 
# información de cada una de estas estaciones 

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
info_rio_maipo = gpd.GeoDataFrame(
        info_rio_maipo, geometry=gpd.points_from_xy(
                info_rio_maipo.longitud.apply(float),
                info_rio_maipo.latitud.apply(float)))

info_rio_maipo.to_file(r'Data_Procesada/estaciones_rio_maipo.geojson',
                       driver='GeoJSON')  

# %%
print('la estación con información más reciente está:')
print(database_rio_maipo.groupby('estacion')['dia'].min().max())
print("""Se deja a discusión si filtramos la información hasta el 2014
      ya que puede ser demasiado reicente""")

database_rio_maipo.to_csv('Data_Procesada/caudales_rio_maipo.csv', index=False,
                       sep=";")
