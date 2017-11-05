from UnimodalGolden import GoldenSectionSearch

import math

def SteepestDescent(startingPoint, GoalFunction, PartialDerivativeFunctions, useGolden=True, epsilon=((0.1)**6)):
  x = startingPoint
  F = GoalFunction
  dF = PartialDerivativeFunctions
  
  gradient = _GetGradientAtPoint(dF, x)
  gradientNorm = _GetGradientNorm(gradient)
  direction = _GetDescentDirection(gradient)
  
  divergenceCounter = 0
  bestValue = 10**6 #a sentinel value
  while _IsGradientNormLarge(gradientNorm, epsilon):
  
    if _IsDiverging(x, F, bestValue, epsilon):
      divergenceCounter += 1
    else:
      bestValue = F(x)
    if divergenceCounter > 100:
      print "Divergence limit has been reached"
      break
      
    KMinimum = 0.1
    if useGolden == True:
      KStartingValue = (0, 1)
      singleDimensionF = _CreateOneDimensionFunction(F, x, direction)
      
      KMinimum = GoldenSectionSearch(KStartingValue, singleDimensionF, epsilon, doUnimodal=True)
      
    for i in range(len(x)):
      x[i] += KMinimum*direction[i]
      
    _PrintDescent(gradientNorm, direction, x)
    
    gradient = _GetGradientAtPoint(dF, x)
    gradientNorm = _GetGradientNorm(gradient)
    direction = _GetDescentDirection(gradient)
      
  return x
    
def _GetGradientAtPoint(dF, x):
  gradient = []
  for partialDerivativeFunction in dF:
    result = partialDerivativeFunction(x)
    gradient.append(result)
    
  return gradient
  
def _GetGradientNorm(gradient):
  sum = 0
  for partialDerivative in gradient:
    sum += partialDerivative**2
    
  return math.sqrt(sum)
    
def _GetDescentDirection(gradient):
  descentDirection = []
  gradientNorm = _GetGradientNorm(gradient)
  for value in gradient:
    descentDirection.append(value / ((-1) * gradientNorm))
    
  return descentDirection

def _IsGradientNormLarge(gradientNorm, epsilon):
  if epsilon < gradientNorm:
    return True
  return False
  
def _IsDiverging(x, F, bestValue, epsilon):
  if (bestValue - epsilon) <= F(x):
    return True
  return False
  
def _CreateOneDimensionFunction(compositeFunction, KPoint, KVector):
  """baseF(x) = x[0]**2           + x[1]**2 is given KPoint = [1 2] and KVector = [3 4]
     compositeF(k) = (1 + 3*k)**2 + (2 + 4*k)**2 is the resulting function"""
  def interdictor(value):
    currentCompositePoint = []
    for i in range(len(KPoint)):
      currentCompositePoint.append(_KFunction(KPoint[i], KVector[i]*value))
    
    calculation = compositeFunction(currentCompositePoint)
    return calculation
    
  return interdictor
  
def _KFunction(a, b):
  return a + b 
  
def _PrintDescent(gradientNorm, direction, x):
  print "-.-.-.-.-.-.-.-.-.-"
  print "gradientNorm:",
  print gradientNorm
  print "direction:",
  print direction
  print "x:",
  print x
  