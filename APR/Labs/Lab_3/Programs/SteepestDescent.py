import math

def SteepestDescent(startingPoint, GoalFunction, PartialDerivativeFunctions, epsilon=((0.1)**6)):
  x = startingPoint
  F = GoalFunction
  dF = PartialDerivativeFunctions
    
  while _IsGradientNormSmall(gradientNorm, epsilon):
    xPrevious = copy(x)
    for i in range(len(x)):
      pass
      #KStartingValue = (0, steps[i])
      
      #compositePoint = _CreateCompositePoint(x, i)
      #KPoint = [x[i], 1]
      #singleDimensionF = _CreateOneDimensionFunction(F, compositePoint, i, KPoint)
      
      #KMinimum = GoldenSectionSearch(KStartingValue, singleDimensionF, epsilon, doUnimodal=True)
      
      #print "Minimum of " + str(compositePoint) + " is " + str(KMinimum)
      
      #x[i] += KMinimum
      
  return x
    
def _GetGradientNorm(gradient):
  sum = 0
  for partialDerivative in gradient:
    sum += partialDerivative**2
    
  return math.sqrt(sum)
  
def _GetGradientAtPoint(dF, x):
  gradient = []
  for partialDerivativeFunction in dF:
    result = partialDerivativeFunction(x)
    gradient.append(result)
    
  return gradient
    
def _IsGradientNormSmall(gradientNorm, epsilon):
  if epsilon > gradientNorm:
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