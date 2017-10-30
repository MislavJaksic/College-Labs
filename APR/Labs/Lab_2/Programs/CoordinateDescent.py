from UnimodalGolden import GoldenSectionSearch
from copy import copy

def CoordinateDescent(startingPoint, GoalFunction, steps=[], epsilon=((0.1)**6)):
  x = startingPoint
  F = GoalFunction
  if not steps:
    for i in range(len(x)):
      steps.append(1)
  xPrevious = copy(x) #for the purpose of checking the while condition
  for i in range(len(x)):
    xPrevious[i] += (i + 1)
    
  while _IsAtLeastOnePointWasMoved(x, xPrevious, epsilon):
    xPrevious = copy(x)
    for i in range(len(x)):
      KStartingValue = (0, steps[i])
      
      compositePoint = _CreateCompositePoint(x, i)
      KPoint = [x[i], 1]
      singleDimensionF = _CreateOneDimensionFunction(F, compositePoint, i, KPoint)
      
      KMinimum = GoldenSectionSearch(KStartingValue, singleDimensionF, epsilon, doUnimodal=True)
      
      print "Minimum of " + str(compositePoint) + " is " + str(KMinimum)
      
      x[i] += KMinimum
      
  return x
    
def _IsAtLeastOnePointWasMoved(x, xPrevious, epsilon):
  for i in range(len(x)):
    if abs(x[i] - xPrevious[i]) > epsilon:
      return True
  return False
  
def _CreateOneDimensionFunction(compositeFunction, compositePoint, KIndex, KPoint):
  """baseF(x) = x[0]         **2 + x[1]**2 is given x = [1 + (2 * k), 3] which transforms baseF(x) into
     compF(k) = (1 + (2 * k))**2 + 3   **2, where KFunction(k) = (1 + (2 * k))"""
  def interdictor(value):
    currentCompositePoint = copy(compositePoint)
    currentCompositePoint[KIndex] = _KFunction(KPoint[0], KPoint[1]*value)
    
    calculation = compositeFunction(currentCompositePoint)
    return calculation
    
  return interdictor
  
def _KFunction(a, b):
  return a + b 
  
def _CreateCompositePoint(x, KIndex):
  compositePoint = copy(x)
  compositePoint[KIndex] = "KFunction"
  return compositePoint
  