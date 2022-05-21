# -*- coding: utf-8 -*-
"""
Created on Thu May 19 14:38:11 2022
Este script busca verificar si hubo un descenso en las precipitaciones
en las estaciones climatológicas del rio maipo
@author: nicos
"""

import pandas as pd
from datetime import datetime, date

# %%
# Se carga la base de datos del cr2
precipitaciones = pd.read_csv('Data/climaticas/cr2_prDaily_2020_ghcn.txt',
                           sep=",", decimal=".", low_memory=False)

# Separamos la información de las estaciones, y sus respectivas mediciones
estaciones = precipitaciones.head(14)
mediciones = precipitaciones.iloc[14:, :]
mediciones['codigo_estacion'] = mediciones.codigo_estacion.apply(
        lambda x: datetime.strptime(x, '%Y-%m-%d').date())


estaciones_names = estaciones.iloc[9, :].reset_index()
estaciones_names.columns = ['codigo', 'estacion']
estaciones_names = estaciones_names.loc[
        pd.notnull(estaciones_names.estacion)]
# Filtramos las estaciones del rio maipo

est_riomaipo = estaciones_names.loc[
        estaciones_names.estacion.apply(lambda x: 'Maipo' in x.split())]
est_riomaipo.set_index('codigo', inplace=True)

# %%
rio_maipo = mediciones.set_index('codigo_estacion')[
        est_riomaipo.index.unique()]

# filtramos el periodo de estudio
rio_maipo = rio_maipo.loc[
        (rio_maipo.index >= date(1980, 1, 1) ) &
        (rio_maipo.index <= date(2019, 12, 31))]


# Realizamos un estudio de las estaciones con mayor disponibilidad de información
mayores_mediciones = pd.DataFrame()
for col in rio_maipo.columns:  
    rio_maipo.loc[rio_maipo[col] == '-9999', col] = None
    mayores_mediciones = mayores_mediciones.append(
            pd.Series([col, pd.notnull(rio_maipo[col]).sum()]),
            ignore_index=True)
mayores_mediciones.columns = ['codigo', 'mediciones']
mayores_mediciones.sort_values('mediciones', ascending=False,
                               ignore_index=True, inplace=True)

# Nos quedamos con las 4 estaciones con mayor información dentro del periodo
mayores_mediciones.head(4)

rio_maipo = rio_maipo[mayores_mediciones.head(4).codigo.unique()]
rio_maipo = rio_maipo.stack().reset_index()

# Tomamos las precipitaciones media por año en estas 4 estaciones
# con mayor información
rio_maipo.columns = ['fecha', 'codigo', 'precipitacion_media']
rio_maipo['year'] = pd.Series(rio_maipo.fecha).apply(
        lambda x: x.year)
rio_maipo['mes'] = pd.Series(rio_maipo.fecha).apply(
        lambda x: x.month)
rio_maipo['precipitacion_media'] = rio_maipo['precipitacion_media'].astype('float')

precipitacion_media = rio_maipo.groupby(
        ['year', 'mes'], as_index=False)['precipitacion_media'].mean()

# Se realizará un estudio en tramos de 10 años.
precipitacion_media['periodo'] = pd.cut(precipitacion_media['year'], [1980, 1990, 2000,
       2010, 2020])
    
# %% Obtenemos las curvas por periodo y separadas por mes para ver el efecto
# de la estacionalidad
    
import seaborn as sns
sns.set_theme(style="darkgrid")
sns.lineplot(x="mes", y="precipitacion_media",
             hue="periodo",
             data=precipitacion_media)