"""All functions have a uniform interface, x is a list"""
import math

def f1(x):
  return 100*((x[1] - (x[0]**2))**2) + ((1 - x[0])**2)
  
def f3(x):
  sum = 0
  for i in range(len(x)):
    sum += (x[i] - i - 1)**2
  return sum
  
def f6(x):
  squareSum = 0
  for i in range(len(x)):
    squareSum += (x[i])**2
  
  return 0.5 + ( (math.sin( math.sqrt(squareSum) )**2) - 0.5) / (1 + 0.001*squareSum)**2
  
def f7(x):
  squareSum = 0
  for i in range(len(x)):
    squareSum += (x[i])**2
    
  return (squareSum**0.25) * (1 + math.sin( 50 * (squareSum**0.1) )**2)