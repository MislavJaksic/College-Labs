from Helpers.UnimodalGolden import GoldenSectionSearch
from Helpers.Matrix import Matrix

import math

def NewtonRaphson(startingPoint, GoalFunction, FirstPartialDerivativeFunctions, SecondPartialDerivativeFunctions, useGolden=True, epsilon=((0.1)**6)):
  x = startingPoint
  F = GoalFunction
  dF = FirstPartialDerivativeFunctions
  ddF = SecondPartialDerivativeFunctions #[[], []] format
  
  gradientMatrix = _GetGradientMatrixAtPoint(dF, x)
  gradientNorm = _GetGradientNorm(gradientMatrix)
  inverseHessianMatrix = _GetInverseHessianMatrixAtPoint(ddF, x)
  
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
    
def _GetGradientMatrixAtPoint(dF, x):
  gradient = []
  for partialDerivativeFunction in dF:
    result = partialDerivativeFunction(x)
    gradient.append(  [result] )
    
  return Matrix(gradient)

def _GetGradientNorm(gradientMatrix):
  gradient = gradientMatrix._GetMatrixColumn(1)
  sum = 0
  for partialDerivative in gradient:
    sum += partialDerivative**2
    
  return math.sqrt(sum)

def _GetInverseHessianMatrixAtPoint(ddF, x):
  hessianValues = []
  for derivativeList in ddF:
    
    results = []
    for derivative in derivativeList:
      results.append(derivative(x))
    hessianValues.append(results)
    
  hessianMatrix = Matrix(hessianValues)
  hessianMatrix.inverse()
  return hessianMatrix

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
  