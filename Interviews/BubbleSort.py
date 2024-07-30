# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 20:29:39 2024

@author: Francisco

Bubble sort - simple but slow
-------------------------------------------------------------------------------
Each pair of adjacent elements is compared and the elements are swapped if they
 are not in order.
***Example: [1,2,8,-3,4,5]
First round  --> n-1 swaps
*** [2,8,1,4,5,-3]
Second round --> n-2 swaps ()

Time Complexity = (n-1) + (n-2)...+2+1 = (n-1)+1 +(n-2+2)...=n * (n-1)/2
BigO(n^2)
Best case BigO(N) --> [-3,8,4,5,2,1]
Average and worse case BigO(n^2)

-------------------------------------------------------------------------------
1.Comienza en el primer elemento de la lista.
2.Compara el elemento actual con el siguiente elemento.
3.Si el elemento actual es mayor que el siguiente, los intercambia.
4.Se mueve al siguiente par de elementos y repite el proceso hasta llegar al 
final de la lista.
5.Vuelve al inicio de la lista y repite el proceso hasta que no se realice 
ningún intercambio en una pasada completa.
"""
import numpy as np

length = np.random.randint(5, 21)
random_array = np.random.randint(1, 101, length)
print(random_array)

for i in np.arange(0,length-1): 
    for j in np.arange(0,length-1-i):
        if random_array[j] < random_array[j+1]:
            random_array[j],random_array[j+1] = random_array[j+1],random_array[j]
            
print(random_array)
