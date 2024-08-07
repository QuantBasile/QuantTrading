# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 20:53:23 2024

@author: Francisco
"""
import matplotlib.pyplot as plt
import pandas as pd

from GetData.FrankfurtBoerse import AbrufData

#NVIDIA US67066G1040
#Deutsche Bank  DE0005140008 

aktie_or_ISIN="US67066G1040"
df=AbrufData(aktie_or_ISIN=aktie_or_ISIN,split=False,dividends=True,Bezugsrechte=True,Date_von="01/01/2023"
             ,Date_bis="01/08/2024")
df2=AbrufData(aktie_or_ISIN=aktie_or_ISIN,split=False,dividends=True,Bezugsrechte=False,Date_von="01/01/2023"
             ,Date_bis="01/08/2024",Boerse="Xetra")


df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%y')
df['Schluss'] = pd.to_numeric((df['Schluss'].str.replace('.','')).str.replace(',','.'))

df2['Datum'] = pd.to_datetime(df2['Datum'], format='%d.%m.%y')
df2['Schluss'] = pd.to_numeric((df2['Schluss'].str.replace('.','')).str.replace(',','.'))

# Plotear los datos
plt.figure(figsize=(10, 5))
plt.plot(df['Datum'], df['Schluss'], marker='o', linestyle='-')
plt.plot(df2['Datum'], df2['Schluss'], marker='x', linestyle='--')
plt.xlabel('Fecha')
plt.ylabel('Schluss')
plt.grid(True)
plt.xticks(rotation=45)

first_date = df['Datum'].dt.date.min()
last_date = df['Datum'].dt.date.max()
plt.title(f'Schluss de {aktie_or_ISIN} von {first_date} bis {last_date}')

plt.tight_layout()
plt.show()