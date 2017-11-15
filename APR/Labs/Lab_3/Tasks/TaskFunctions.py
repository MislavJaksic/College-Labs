"""All functions have a uniform interface, x is a list"""

def f1(x):
  return 100*((x[1] - (x[0]**2))**2) + ((1 - x[0])**2)
  
def df1x0(x):
  return (400*x[0]**3 + 2*x[0] - 200*x[1] - 2)
  
def ddf1x0x0(x):
  return (1200*x[0]**2 + 2)
  
def df1x1(x):
  return (200*x[1] - 200*x[0])
  
def ddf1x1x1(x):
  return 200
  
def ddf1x0x1(x):
  return (-200)
  
  
  
def f2(x):
  return ((x[0] - 4)**2) + 4*((x[1] - 2)**2)
  
def df2x0(x):
  return (2*x[0] - 8)
  
def ddf2x0x0(x):
  return (2)
  
def df2x1(x):
  return (8*x[1] - 16)
  
def ddf2x1x1(x):
  return (8)
  
def ddf2x0x1(x):
  return (0)
  
  
  
def f3(x):
  return ((x[0] - 2)**2) + ((x[1] + 3)**2)
  
def df3x0(x):
  return (2*x[0] - 4)
  
def ddf3x0x0(x):
  return (2)
  
def df3x1(x):
  return (2*x[1] + 6)
  
def ddf3x1x1(x):
  return (2)
  
def ddf3x0x1(x):
  return (0)
  
  
  
def f4(x):
  return ((x[0] - 3)**2) + ((x[1])**2)
  
  
  
def constraint1(x):
  return x[1] - x[0]
  
def constraint2(x):
  return 2 - x[0]
  
def constraint3(x):
  return 3 - x[0] - x[1]
  
def constraint4(x):
  return 3 - 1.5 * x[0] - x[1]
 
def constraint5(x):
  return x[1] - 1

  
def constraint6(x):
  return 100 - x[0]
  
def constraint7(x):
  return x[0] + 100
  
def constraint8(x):
  return 100 - x[1]
  
def constraint9(x):
  return x[1] + 100