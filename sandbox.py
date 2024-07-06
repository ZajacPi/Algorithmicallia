import numpy as np

coefficients = input().split()
list_of_coeff = [float(i) for i in coefficients]
x = float(input())
print(np.polyval(list_of_coeff, x))