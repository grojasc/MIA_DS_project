# -*- coding: utf-8 -*-
"""
A partir del proceso de forecasting realizado en R
Entrega el output de la oferta de volumen de agua disponible en el Rio Maipo
estación manzano
y se consolida junto con la información histórica elaborada en
caudales_manzano.py
@author: nicos
"""

import pandas as pd
import calendar
from caudales_manzano import manzano

# %%
# Cargamos la predicción de caudales hasta 2030
predicciones_caudal = pd.read_csv(
        'Data_Procesada/prediccion_caudales_2030.csv')
predicciones_caudal.columns = [
        'fecha', 'forecast', 'Lo.80', 'Hi.80', 'Lo.95', 'Hi.95']

# Obtendremos el volumen disponible mensual por estos caudales
# Para esto primero dejamos en formato fecha este dataset y luego
# obtenemos la cantidad de días por mes.
predicciones_caudal['mes'] = predicciones_caudal.fecha.apply(
        lambda x: x.split()[0])

predicciones_caudal['dias'] = predicciones_caudal['mes'].replace(
        {'Dec':'31', 'Jan':'31', 'Feb':'28', 'Mar':'31', 'Apr':'30',
         'May':'31', 'Jun':'30', 'Jul':'31', 'Aug':'31',
       'Sep':'30', 'Oct':'31', 'Nov':'30'}).apply(int)
predicciones_caudal['year'] = predicciones_caudal.fecha.apply(
        lambda x: x.split()[1])

# Obtenemos el volumen en m3 de agua disponibles por mes
predicciones_caudal['volumen m3'] = predicciones_caudal.apply(
        lambda x: x.forecast * 3600* 24 * x.dias, axis=1)

# agrupamos esta información por año de proyección
predicciones_output = predicciones_caudal.groupby(
        ['year'], as_index=False)['volumen m3'].sum()

# %% Obtendremos un simil output para la información histórica

manzano_agg = manzano.copy()
manzano_agg['mes'] = manzano.dia.apply(lambda x: x.month)
manzano_agg = manzano_agg.groupby(['year', 'mes'],
                                  as_index=False)['caudal'].mean()
manzano_agg['dias'] = manzano.dia.apply(lambda x: calendar.monthrange(
        x.year,x.month)[1])
manzano_agg['volumen m3'] = manzano_agg.apply(
        lambda x: x.caudal * 3600 * 24 * x.dias, axis=1)
manzano_agg = manzano_agg.loc[manzano_agg.year >= 1980]

manzano_output = manzano_agg.groupby(
        'year', as_index=False)['volumen m3'].sum()

# como a los datos del manzano le falta diciembre se lo agregamos de la proyección


manzano_output.loc[
        manzano_output.year ==2021, 'volumen m3'] = (
        manzano_output.loc[
        manzano_output.year ==2021, 'volumen m3'].values[0] + 
        predicciones_output.loc[
        predicciones_output.year.apply(int) == 2021, 'volumen m3']\
                .values[0])

# %% Se hará un plot con la evolución de volumen disponible con información
# histórica y proyectada

manzano_output['origen'] = 'medicion'
predicciones_output['origen'] = 'time-series forecast'
caudales_output = manzano_output.append(
        predicciones_output.loc[predicciones_output.year.apply(int)>=2022],
        ignore_index=True)
caudales_output['year'] = caudales_output['year'].apply(int)

# %%
import seaborn as sns
sns.set_theme(style="darkgrid")
sns.lineplot(x="year", y="volumen m3",
             hue="origen",
             data=caudales_output)
# %%
# Se exporta esta información para relacionarla con la regresión de demanda
# de agua potable

caudales_output.to_excel('resultados oferta de agua.xlsx')