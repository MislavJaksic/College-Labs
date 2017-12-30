from UnimodalGolden import GoldenSectionSearch
from copy import copy

def CoordinateDescent(startingPoint, GoalFunction, steps=[], epsilon=((0.1)**6)):
  x = startingPoint
  F = GoalFunction
  if not steps:
    for i in range(len(x)):
      steps.append(1)
  xPrevious = copy(x)
  for i in range(len(x)):
    xPrevious[i] += (i + 1)
    
  while _IsAtLeastOnePointWasMoved(x, xPrevious, epsilon):
    
    xPrevious = copy(x)
    for descentDimension in range(len(x)):
      singleDimensionF = _CreateOneDimensionFunction(F, x, descentDimension)
      
      KStartingValue = (0, steps[descentDimension])
      KMinimum = GoldenSectionSearch(KStartingValue, singleDimensionF, epsilon, doUnimodal=True)
      
      print "Add " + str(KMinimum) + " to " + str(x[descentDimension])
      
      x[descentDimension] += KMinimum
      
  return x
    
def _IsAtLeastOnePointWasMoved(x, xPrevious, epsilon):
  for i in range(len(x)):
    if abs(x[i] - xPrevious[i]) > epsilon:
      return True
  return False
  
def _CreateOneDimensionFunction(F, x, descentDimension):
  """F(x) = x[0]         **2 + x[1]**2 and x[0]=(1 + (2 * k)) and x[1]=3 into
     F(k) = (1 + (2 * k))**2 + 3   **2, where KFunction(k) = (1 + (2 * k))"""
  def interdictor(value):
    compositePoint = copy(x)
    compositePoint[descentDimension] = _KFunction(x[descentDimension], value)
    
    calculation = F(compositePoint)
    return calculation
    
  return interdictor
  
def _KFunction(a, b):
  return a + b
  