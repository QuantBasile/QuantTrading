# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 19:40:45 2024

@author: Francisco
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from GetData.FrankfurtBoerse import AbrufData
from GetData.Discrete import Tchebysheff

aktie_or_ISIN="DE0005140008"
df=AbrufData(aktie_or_ISIN=aktie_or_ISIN,split=False,dividends=True,Bezugsrechte=True,Date_von="01/01/2023"
             ,Date_bis="01/08/2024")

df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%y')
df['Schluss'] = pd.to_numeric((df['Schluss'].str.replace('.','')).str.replace(',','.'))

mu=np.average(df['Schluss'])
sigma=np.sqrt(((df['Schluss']-mu)**2).sum())
Tchebysheff(mu=mu,sigma=sigma,k=1)

# Predict if tomorrow the price will go up or down 
df['Return_day'] = df['Schluss'] - df['Schluss'].shift(1)

df_binary = (df['Return_day'] > 0).astype(int)
