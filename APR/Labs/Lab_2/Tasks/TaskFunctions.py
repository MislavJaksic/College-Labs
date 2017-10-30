"""All functions have a uniform interface, x is a list"""

def f1(x):
  return 100*((x[1] - (x[0]**2))**2) + ((1 - x[0])**2)
  
def f2(x):
  return ((x[0] - 4)**2) + 4*((x[1] - 2)**2)
  
def f3(x):
  sum = 0
  for i in range(len(x)):
    sum += (x[i] - i)**2
  return sum
  
def f4(x):
  return math.abs(((x[0] - x[1])*(x[0] + x[1]))) + math.sqrt((x[0]**2) + (x[1]**2))
  
def f6(x):
  squareSum = 0
  for i in range(len(x)):
    squareSum += (x[i])**2
  
  return 0.5 + ( (math.sin( math.sqrt(squareSum) )**2) - 0.5) / (1 + 0.001*squareSum)**2
  