# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 19:39:20 2024

@author: Francisco
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 20:53:23 2024

@author: Francisco
"""
import numpy as np
import pandas as pd
import math


def Tchebysheff(mu=0, sigma=1, k=1):
    if k <1:
        raise ValueError("The value K cannot be smaller than 1.")
    limit1=mu-k*sigma
    limit2=mu+k*sigma
    print(f"P({limit1}<X<{limit2} >= {1-1/k**2}")
    return

def Bernoulli(data):
    """
    Calculate the probability function of a Bernoulli distribution.

    Parameters:
    Data that is either 0 or 1

    Returns:
    p: probability of success (1)
    e: expected value
    v: variance
    """
    if not data.isin([0, 1]).all().all():
        raise ValueError("x must be either 0 or 1.")
    
    size = len(data)
    p=data.sum()/size #success or 1
    print(f"Probability of success is {p}")
    print(f"Expected value is {p}")
    print(f"Variance is {p*(1-p)}")
    
def Binomial(data,Y=1,N=1): 
    """
    Calculate the probability function of a Binomial distribution.

    Parameters:
    Data that is either 0 or 1
    y: numbers of success we are looking for
    n: indepedent measurements we do in the sample

    Returns:
    p(y): probability of reaching Y successes in sample
    p: probability of success (1)
    e: expected value
    v: variance
    
    p(y,n): 3d plot
    """
    if not data.isin([0, 1]).all().all():
        raise ValueError("x must be either 0 or 1.")
    
    size = len(data)
    p=data.sum()/size #success or 1
    prob= math.comb(N, Y)*(p**Y)*(1-p)**(N-Y)
    E=N*p
    V=N*p*(1-p)
    
    n_values = np.arange(1, size+1)  # Valores de n
    y_values = np.arange(0, size+1)  # Valores de y
    p_y_n = np.array([[math.comb(n_i, y_j) * (p**y_j) * ((1-p)**(n_i-y_j)) if y_j <= n_i else 0
                 for n_i in n_values] for y_j in y_values])
    
    return prob,E,V,p,p_y_n,n_values,y_values

def Geometric(data,Y=1): 
    """
    Calculate the probability function of a Geometric distribution.

    Parameters:
    Data that is either 0 or 1
    Y: number of the trial on which the first success happens

    Returns:
    p(Y=y): probability of having the first success in Y
    p: probability of success (1)
    e: expected value
    v: variance
    """
    if not data.isin([0, 1]).all().all():
        raise ValueError("x must be either 0 or 1.")
    
    size = len(data)
    p=data.sum()/size #success or 1
    P_Y_y=((1-p)**(Y-1))*p
    
    print(f"Probability of having the first success in {Y} is {P_Y_y}")
    print(f"Expected value is {1/p}")
    print(f"Variance is {(1-p)/(p**2)}")
