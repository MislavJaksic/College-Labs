"""All functions have a uniform interface, x is a list"""

def f1(x):
  return 100*((x[1] - (x[0]**2))**2) + ((1 - x[0])**2)
  
def df1x0(x):
  return (400*x[0]**3 + 2*x[0] - 200*x[1] - 2)
  
def df1x1(x):
  return (200*x[1] - 200*x[0])
  
  
  
def f2(x):
  return ((x[0] - 4)**2) + 4*((x[1] - 2)**2)
  
def df2x0(x):
  return (2*x[0] - 8)
  
def df2x1(x):
  return (8*x[1] - 16)
  
  
  
def f3(x):
  return ((x[0] - 2)**2) + ((x[1] + 3)**2)
  
def df3x0(x):
  return (2*x[0] - 4)
  
def df3x1(x):
  return (2*x[1] + 6)
  
  
  
def f4(x):
  return ((x[0] - 3)**2) + ((x[1])**2)
  