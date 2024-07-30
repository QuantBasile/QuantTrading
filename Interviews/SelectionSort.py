# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 22:00:36 2024

@author: Francisco
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 20:29:39 2024

@author: Francisco

Selection sort
-------------------------------------------------------------------------------
Repeatadly find the minimum element from unsorted part and putting it at the 
beginning.

-------------------------------------------------------------------------------
1.Encuentra el elemento mínimo en la parte no ordenada de la lista.
2.Intercambia este elemento mínimo con el primer elemento de la parte no 
ordenada.
3.Mueve el límite entre la parte ordenada y la parte no ordenada un lugar 
hacia la derecha.
4.Repite los pasos anteriores hasta que toda la lista esté ordenada.
"""

import numpy as np

length = np.random.randint(5, 10)
random_array = np.random.randint(1, 101, length)
print(random_array)

for i in range(0,length):
    min_index= i
    
    for j in range(i+1,length): # take all the part  that is unordered
        if random_array[j]< random_array[min_index]:
            min_index=j
    
    random_array[min_index],random_array[i]=random_array[i],random_array[min_index]
    print(f"i = {i}",random_array)
