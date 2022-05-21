# -*- coding: utf-8 -*-
"""
Created on Thu May 19 14:47:20 2022

@author: Dinde
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Inicializacion y normalizacion
dataset         = pd.read_excel('dataset_demanda.xlsx', index_col=0).interpolate(axis='index')

data_train   = dataset.loc[:2020].iloc[:,:-1].to_numpy()
data_labels  = dataset.loc[:2020].iloc[:,-1].to_numpy()*1000 

data_predict = dataset.loc[2021:].iloc[:,:-1].to_numpy()

dataset_predict = pd.read_excel('dataset_demanda.xlsx', index_col=0)


# Modelo de regresion
model = LinearRegression()
model.fit(np.arange(2009,2021).reshape(-1,1), data_labels)

y_predict = model.predict(np.arange(2021,2036).reshape(-1,1))

a = pd.DataFrame( np.concatenate( (np.arange(2021,2036).reshape(-1,1),y_predict.reshape(-1,1)), axis=1) , columns = ['año','demanda de agua'])
a.to_excel('demanda_agua 2021-2035.xlsx')

df = pd.read_excel('dataset_demanda2.xlsx')
year = pd.Series(np.arange(2022,2050)).rename('año')
year.index = np.arange(13,13+28)

model = LinearRegression()
model.fit(df['año'].to_numpy().reshape(-1,1), df['porcentaje'])

prediction = model.predict(np.arange(2022,2100).reshape(-1,1))
prediction = np.concatenate((np.arange(2022,2100).reshape(-1,1), prediction.reshape(-1,1) ), axis=1) 

# ------------------ Output prediccion y grafico lindo ------------------------------------

pd.DataFrame(prediction, columns=['año', 'porcentaje de uso']).to_excel('porcentaje de uso prediccion.xlsx')
fig, ax = plt.subplots( figsize=(10,8))

sns.lineplot(x='año', y='porcentaje', data=df, ax=ax, label=r'Porcentaje de uso')
sns.lineplot(x = np.linspace(2008,2036), y = model.predict(np.linspace(2010,2036).reshape(-1,1)), ax=ax, label='Regresión')
plt.savefig('regression_por_de_uso.png')








