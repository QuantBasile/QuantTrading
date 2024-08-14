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
    

