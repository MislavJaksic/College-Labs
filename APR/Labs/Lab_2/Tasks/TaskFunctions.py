def f1(x1, x2):
  return 100*((x2 - (x1**2))**2) + ((1 - x1)**2)
  
def f2(x1, x2):
  return ((x1 - 4)**2) + 4*((x2 - 2)**2)
  
def f3(xi):
  sum = 0
  for i in range(len(xi)):
    sum += (xi[i] - i)
  return sum
  
def f4(x1, x2):
  return math.abs(((x1 - x2)*(x1 + x2))) + math.sqrt((x1**2) + (x2**2))
  
def f6(xi):
  squareSum = 0
  for i in range(len(xi)):
    squareSum += (xi[i])**2
  
	return 0.5 + ( (math.sin( math.sqrt(squareSum) )**2) - 0.5) / (1 + 0.001*squareSum)**2
  