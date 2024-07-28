# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 20:53:23 2024

@author: Francisco
"""
import matplotlib.pyplot as plt
import pandas as pd

from GetData.FrankfurtBoerse import AbrufData

df=AbrufData()
df2=AbrufData(Boerse="Xetra")


df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%y')
df['Schluss'] = pd.to_numeric(df['Schluss'].str.replace(',', '.'))

df2['Datum'] = pd.to_datetime(df2['Datum'], format='%d.%m.%y')
df2['Schluss'] = pd.to_numeric(df2['Schluss'].str.replace(',', '.'))

# Plotear los datos
plt.figure(figsize=(10, 5))
plt.plot(df['Datum'], df['Schluss'], marker='o', linestyle='-')
plt.plot(df2['Datum'], df2['Schluss'], marker='x', linestyle='--')
plt.xlabel('Fecha')
plt.ylabel('Schluss')
plt.title('Schluss de Deutsche Bank AG')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()