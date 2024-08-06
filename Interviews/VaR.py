# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 17:06:59 2024

@author: Francisco
"""

"""
Created on Tue Jul 30 20:29:39 2024

@author: Francisco

VaR
-------------------------------------------------------------------------------
Assume Gaussian Distribution for expected returns.
Calculate VaR 95%

-------------------------------------------------------------------------------
need to solve integral(from X to +inf) of probability = 95%
Normally people use Z score
Lets do with formulas here
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.special import erf, erfinv

mu = 0.0      # Media
sigma = 0.1 # Desviación estándar
p=0.99 # Probability for VaR

def normal_gaussian(x, mu=0, sigma=1):
    """
    https://en.wikipedia.org/wiki/Normal_distribution
    https://en.wikipedia.org/wiki/Normal_distribution#Standard_normal_distribution
    """
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)



# Definir la función de distribución acumulativa (CDF) usando integración numérica
def normal_cdf(x, mu, sigma):
    """
    Probability that a number, arising from a standard normal distribution,
    lies between -inf and x
    """
    return quad(normal_gaussian, -np.inf, x, args=(mu, sigma))[0]

def normal_cdf_err(x, mu, sigma):
    """
    https://en.wikipedia.org/wiki/Cumulative_distribution_function
    """
    return 0.5 * (1 + erf((x - mu) / (sigma * np.sqrt(2))))

def probit(p, mu, sigma):
    """
    Inverse of cdf. Maps a probability (p) to an x value from the 
    standard normal distribution
    https://en.wikipedia.org/wiki/Probit
    """
    return mu + sigma * np.sqrt(2) * erfinv(2 * p - 1)

VaR=probit(p, mu, sigma)
ES = mu + sigma * normal_gaussian(probit(p, mu=0, sigma=1),mu=0,sigma=1) / (1 - p)#also cVaR pdf(1-p)=pdf(p)


#Density function of expected returns
x = np.linspace(mu - 6*sigma, mu + 6*sigma, 1000)
plt.plot(x,normal_gaussian(x,mu,sigma))
plt.axvline(x=ES, color='g', linestyle='--', label=f'cVaR for 95% --> \n {ES:0.5f}')
plt.axvline(x=VaR, color='r', linestyle='--', label=f'VaR for 95% --> \n {VaR:0.5f}')
plt.xlabel('Expected returns per day')
plt.ylabel('Frequency')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

print("Check equal weighing of cVaR")
print(f"Primer tramo {quad(normal_gaussian, VaR, ES, args=(mu, sigma))[0]}")
print(f"Segundo tramo {quad(normal_gaussian, ES, np.inf, args=(mu, sigma))[0]}")
print(f"Tramo total {quad(normal_gaussian, VaR, np.inf, args=(mu, sigma))[0]}")