# -*- coding: utf-8 -*-
"""
Created on Thu May 19 11:17:07 2022
Este script busca verificar si hubo un descenso en las precipitaciones
en las estaciones climatológicas del rio maipo
@author: nicos
"""

import pandas as pd
from datetime import datetime, date
# %% Se carga la base de datos del cr2
temperaturas = pd.read_csv('Data/climaticas/cr2_tasDaily_2020_ghcn.txt',
                           sep=",", decimal=".", low_memory=False)


# %%

# Separamos la información de las estaciones, y sus respectivas mediciones
estaciones = temperaturas.head(14)
mediciones = temperaturas.iloc[14:, :]
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
        (rio_maipo.index >= date(2000, 1, 1) ) &
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

# Tomamos las temperaturas media por año en estas 4 estaciones
# con mayor información

rio_maipo.columns = ['fecha', 'codigo', 'temperatura_media']
rio_maipo['year'] = pd.Series(rio_maipo.fecha).apply(
        lambda x: x.year)
rio_maipo['mes'] = pd.Series(rio_maipo.fecha).apply(
        lambda x: x.month)
rio_maipo['temperatura_media'] = rio_maipo['temperatura_media'].astype('float')

temperaturas_medias = rio_maipo.groupby(
        ['year', 'mes'], as_index=False)['temperatura_media'].mean()

# Se realizará un estudio en tramos de 10 años.
temperaturas_medias['periodo'] = pd.cut(temperaturas_medias['year'], [2000,
       2010, 2020])
    
# %% Obtenemos las curvas por periodo y separadas por mes para ver el efecto
# de la estacionalidad
    
import seaborn as sns
sns.set_theme(style="darkgrid")
sns.lineplot(x="mes", y="temperatura_media",
             hue="periodo",
             data=temperaturas_medias)
