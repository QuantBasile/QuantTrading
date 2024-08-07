"""
Created on Tue Jul 30 20:29:39 2024

@author: Francisco

You roll a die 100 times and add the results. Find the minimum range of values 
that you are 95% sure that the sum will fall within the range.
-------------------------------------------------------------------------------
Central limit theorem --> Assume Gaussian distribution centered at 3.5*N and 
variance of variance of a roll*N

-------------------------------------------------------------------------------
need to solve integral(from a to b) of probability = 95%
Normally people use Z score
"""
import numpy as np
import matplotlib.pyplot as plt


N=100
mu=3.5*N
var=sum((x-3.5)**2 for x in [1,2,3,4,5,6])*N

sigma=np.sqrt(var)

x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)

#corregir sigma
y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


plt.plot(x, y, label=f'Gaussian Distribution\n$\mu={mu}$, $\sigma={sigma}$')
plt.xlabel('X')
plt.ylabel('Probability Density')
plt.title('Gaussian Distribution')
plt.legend()
plt.grid(True)
plt.show()


import numpy as np
from scipy.stats import norm

# Definir el percentil
percentil_97_5 = 0.975

# Calcular el valor crítico Z usando la función ppf
z_score = norm.ppf(percentil_97_5)

print(f"Valor crítico Z para un intervalo de confianza del 95%: {z_score}")



from scipy.integrate import quad

# Definir la función de densidad de probabilidad de la distribución normal estándar
def normal_pdf(x):
    return (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)

# Calcular el área bajo la curva desde -1.96 a 1.96
area, _ = quad(normal_pdf, -1.96, 1.96)

print(f"Área bajo la curva de -1.96 a 1.96: {area}")
