from copy import copy

def HookeJeeves(startingPoint, GoalFunction, steps=[], epsilon=(0.1)**6):
  """startingPoint is a Python list"""
  xb = xp = xn = []
  xb = xp = startingPoint
  F = GoalFunction
  if not steps:
    for i in range(len(xb)):
      steps.append(0.5)
  print "xb     xp     xn     condition     steps[0]"
  
  while(steps[0] > epsilon):
    xn = _FindBestStepPoint(xp, steps, F)
    _PrintRow(xb, xp, xn, F, steps[0])
    
    if _IsXBFartherFromMinThenXN(xb, xn, F):
      xp = _ReflectXBAccrossXN(xb, xn)
      xb = xn
    else:
      steps = _HalveSteps(steps)
      xp = xb
      
  return xb
     
def _FindBestStepPoint(xp, steps, F):
  bestPoint = copy(xp)
  for i in range(len(bestPoint)): 
    plusPoint = _CalculateStepPoint(bestPoint,       steps[i], i)
    zeroPoint = _CalculateStepPoint(bestPoint,              0, i)
    minusPoint = _CalculateStepPoint(bestPoint, (-1)*steps[i], i)
    
    if F(minusPoint) < F(zeroPoint):
      bestPoint = minusPoint
    elif F(zeroPoint) < F(plusPoint):
      bestPoint = zeroPoint
    else:
      bestPoint = plusPoint
      
  return bestPoint

def _CalculateStepPoint(x, step, coordinate):
  stepPoint = copy(x)
  stepPoint[coordinate] += step
  return stepPoint

def _IsXBFartherFromMinThenXN(xb, xn, F):
  if F(xb) > F(xn):
    return True
  return False

def _ReflectXBAccrossXN(xb, xn):
  reflectedPoint = []
  for i in range(len(xb)):
    reflectedPoint.append(2*xn[i] - xb[i])
  
  return reflectedPoint

def _HalveSteps(steps):
  halvedSteps = []
  for i in range(len(steps)):
    halvedSteps.append(steps[i] / 2.)
  
  return halvedSteps
  
def _PrintRow(xb, xp, xn, F, step):
  row = ""
  row += str(xb)
  row += str(xp)
  row += str(xn)
  row += "  "
  row += str(F(xb)) + ">" + str(F(xn))
  row += "  "
  row += str(step)
  print row