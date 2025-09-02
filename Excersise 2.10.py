from numpy import *
from matplotlib import *
import numpy as np
import matplotlib.pyplot as plt

def V(r, x): #We define the potential function 
    a = 1.0  #Fix variables a and v
    v = 2.0
    return v * (r/a)**x #the operation to realice 

radius = range(1, 6) #We define a range for variables radius and exponent
exponent = range(0, 11) 

for r in radius: #make "for" cicle that take the distints values of r
    for x in exponent: #make another "for" cicle inside to repeat each one of radius and exponents
        result = V(r, x) #rename V to results
        print(f"V(r={r}, x={x}) = {result:.2f}") #print using f'' to include directly the variables

# for make graphics

x_values = np.linspace(0, 10, 1000)  #We establish steps of 1000 pointss between 0 and 10

plt.figure(figsize=(20, 7)) #size of the figure

#For the variable exponent with radius fixed
plt.subplot(1, 2, 1) 
for r in radius:
    V_values = [V(r, x) for x in x_values]  
    plt.plot(x_values, V_values, label=f'r = {r}', linewidth=2)

plt.xlabel('Exponente (k)')
plt.ylabel('V(k)')
plt.title('V(k) for distincts radius r')
plt.grid(True, alpha=0.3)
plt.legend()