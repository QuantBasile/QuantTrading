# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 19:40:45 2024

@author: Francisco
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from GetData.FrankfurtBoerse import AbrufData
from Stats.Discrete import Tchebysheff
from Stats.Discrete import Bernoulli
from Stats.Discrete import Binomial
from Stats.Discrete import Geometric
from mpl_toolkits.mplot3d import Axes3D
import math
from scipy.stats import binom

# Get data --------------------------------------------------------------------
aktie_or_ISIN="DE0005140008"
df=AbrufData(aktie_or_ISIN=aktie_or_ISIN,split=False,dividends=True,
             Bezugsrechte=True,Date_von="01/01/2023",Date_bis="01/08/2024")
df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%y')
df['Schluss'] = pd.to_numeric((df['Schluss'].str.replace('.','')).str.replace(',','.'))

# Calculate properties of this distribution -----------------------------------
mu=np.average(df['Schluss'])
sigma=np.sqrt(((df['Schluss']-mu)**2).sum())
Tchebysheff(mu=mu,sigma=sigma,k=1)

# Predict if tomorrow the price will go up or down ----------------------------
df['Return_day'] = df['Schluss'] - df['Schluss'].shift(1)
df_binary = (df['Return_day'] > 0).astype(int)
Bernoulli(df_binary)

# Probability of having n independent (in theory) days with positive return (y)
N,Y=150,75
prob,E,V,p,p_y_n,n_values,y_values=Binomial(df_binary,Y=Y,N=N)
print(f"Probability of positive return of 75 days given we consider 150 is {prob}")
if abs(prob-binom.pmf(Y, N, p)) >0.000001:
    raise ValueError(f"Official library disagrees with {binom.pmf(Y, N, p)}")

# Probability of having at least n independent (in theory) days with positive return (y)
prob_Y= pd.DataFrame(np.arange(0,N+1), columns=['Number of succeses'])
prob_Y['Probability'] = prob_Y['Number of succeses'].apply(
    lambda i: Binomial(df_binary, Y=i, N=N)[0])


# Plotting binomial distribution 3D
prob,E,V,p,p_y_n,n_values,y_values=Binomial(df_binary)
n, y = np.meshgrid(n_values, y_values)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(n, y, p_y_n, cmap='viridis')
ax.set(xlabel='Número de ensayos (n)', ylabel='Número de éxitos (y)', zlabel='Probabilidad P(Y=y)', 
       title='Distribución Binomial 3D', 
       xlim=(min(n_values), max(n_values)), 
       ylim=(min(y_values), max(y_values)), 
       zlim=(0, np.max(p_y_n))) 
plt.show()

# Plotting binomial distribution 2D
p_y_N = [math.comb(N, y_i) * (p**y_i) * ((1-p)**(N-y_i)) for y_i in y_values]
p_n_Y= [math.comb(n_i, Y) * (p**Y) * ((1-p)**(n_i-Y)) for n_i in n_values]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
ax1.plot(y_values, p_y_N, marker='o')
ax1.set(xlabel='Number of successes (y)', ylabel='Probability P(y,n=N)', 
        title=f'Probability of finding y successes for fixed n={N}')
ax1.grid(True)
ax2.plot(n_values, p_n_Y, marker='o')
ax2.set(xlabel='Number of Trials (n)', ylabel='Probability P(Y=y,n)',
        title=f'Probability of finding {Y} successes for a given n')
ax2.grid(True)
plt.tight_layout()
plt.show()

# Probability of having the first success in the Y day
Geometric(df_binary,Y=3)