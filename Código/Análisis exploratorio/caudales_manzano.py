# -*- coding: utf-8 -*-
"""
Created on Tue May 17 22:00:17 2022
consolidación caudales
@author: nicos
"""
import pandas as pd
from datetime import date, datetime
import os
# %%
# Se cargan los datos

caudales_historica = pd.read_csv('Data_Procesada/caudales_rio_maipo.csv',
                                 sep=";")
caudales_nueva = pd.read_csv('Data_Procesada/caudales_2018-2021.csv',
                             index_col = 0)

# %%
estaciones = pd.read_csv(os.path.join(
        'Data',  'cr2_qflxDaily_2018_stations.txt'), sep=",", decimal=".",
        low_memory=False)
#agregamos el nombre de la estacion a la información historica cr2
caudales_historica = caudales_historica.merge(
        estaciones[['codigo_estacion', 'nombre']], left_on='estacion',
        right_on='codigo_estacion')


# Dejamos ambas bases en formatos iguales fecha, caudal, nombre_estacion

caudales_nueva = caudales_nueva.loc[pd.notnull(caudales_nueva.Caudal)]
caudales_nueva['mes'] = caudales_nueva['mes'].replace(
        {'March':'3', 'April':'4', 'May':'5', 'June':'6', 'July':'7',
         'August':'8', 'September':'9', 'October':'10', 'November':'11',
         'December' : '12', 'January':'1', 'February':'2'})

caudales_nueva['mes'] = caudales_nueva['mes'].astype('int')
caudales_nueva['day'] = caudales_nueva['day'].astype('int')

caudales_nueva['fecha'] = caudales_nueva.apply(lambda x:
    date(x.year, x.mes, x.day), axis=1)

caudales_nueva = caudales_nueva[['fecha', 'Caudal', 'nombre']]
caudales_historica = caudales_historica[['dia', 'caudal', 'nombre']]
caudales_nueva.columns = caudales_historica.columns

# %%
#Se estudia la disponibilidad de información en las estaciones

caudales_historica['nombre'] = caudales_historica['nombre'].apply(
        lambda x: x.upper())
caudales_historica['dia'] = caudales_historica['dia'].apply(
        lambda x: datetime.strptime(x, '%Y-%m-%d').date())


nueva_filtrada = caudales_nueva.loc[
        caudales_nueva.nombre.isin(caudales_historica.nombre)]
nueva_filtrada = nueva_filtrada[~nueva_filtrada.nombre.isin(
        ['QUEBRADA RAMON EN RECINTO EMOS', 'RIO MAIPO EN LAS HUALTATAS',
         'ESTERO PUANGUE EN RUTA 78'])]


historica_filtrada = caudales_historica.loc[
        ((caudales_historica.nombre.isin(nueva_filtrada.nombre)) &
         (caudales_historica.dia <date(2018, 3, 1)))]

# %%
historica_filtrada.groupby('nombre')['dia'].max()
nueva_filtrada.groupby('nombre')['dia'].min()


historica_filtrada.groupby('nombre')['dia'].min()
nueva_filtrada.groupby('nombre')['dia'].max()

# %% 
# Se opta por la estación manzana dada su ubicación geográfica y mayor cantidad
# de mediciones
manzano = historica_filtrada.append(nueva_filtrada, ignore_index=True)
manzano = manzano.loc[manzano.nombre == 'RIO MAIPO EN EL MANZANO']\
    .reset_index(drop=True)
manzano.loc[manzano.caudal == -9999, 'caudal'] = None

# %%
# Se exporta esta información para disponibilizarla para tareas de exploración
manzano.to_csv('caudales estacion manzano.csv',
               index=False)

# %% Vamos a hacer un plot del descenso de caudales en tramos de 10 años

manzano['year'] = manzano['dia'].apply(lambda x: x.year)
manzano_plot = manzano.loc[manzano.year>=1980]

manzano_plot['mes'] = manzano_plot['dia'].apply(lambda x: x.month)
manzano_plot['periodo'] = pd.cut(manzano_plot['year'], [1980, 1990, 2000,
       2010, 2020, 2030])

# %% Obtenemos las curvas por periodo y separadas por mes para ver el efecto
# de la estacionalidad
    

import seaborn as sns
sns.set_theme(style="darkgrid")
sns.lineplot(x="mes", y="caudal",
             hue="periodo",
             data=manzano_plot)
