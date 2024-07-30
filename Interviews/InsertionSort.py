# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 21:27:03 2024

@author: Francisco
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 20:29:39 2024

@author: Francisco

Insertion sort - simple but slow
-------------------------------------------------------------------------------
Like bubble sort.
For an interation, it compares the given array to all the others and if
condition is met, it pushes the value to the right. 
At the end of the iteration, the given array is inserted in the right position


Time Complexity = BigO(n^2)
Best case BigO(N)
Average and worse case BigO(n^2)
-------------------------------------------------------------------------------
1.Comienza con el primer elemento (se asume que está ordenado).
2.Toma el siguiente elemento y lo inserta en la posición correcta en la parte 
ya ordenada.
3.Repite el paso 2 hasta que todos los elementos estén ordenados.
"""
import numpy as np

length = np.random.randint(5, 10)
random_array = np.random.randint(1, 101, length)
print(random_array)

for i in range(0,length-1):
    key_item = random_array[i]  # array to be inserted
    
    j=i-1 # run through the rest of the array that is already ordered
    while j>= 0 and random_array[j] > key_item:
        random_array[j+1] = random_array[j] #find the position to be inserted
        print(f"i={i},j={j}",random_array)
        j-=1
    
    random_array[j+1]= key_item #insert it
    print(f"i={i}",random_array)