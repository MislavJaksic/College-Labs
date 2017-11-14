from Helpers.UnimodalGolden import GoldenSectionSearch
from Helpers.Matrix import Matrix

import math

def NewtonRaphson(startingPoint, GoalFunction, FirstPartialDerivativeFunctions, HessianPartialDerivativeFunctions, useGolden=True, epsilon=((0.1)**6)):
  x, F, dF, ddF = _MapToMathsNames(startingPoint, GoalFunction, FirstPartialDerivativeFunctions, HessianPartialDerivativeFunctions)
  
  gradient = _CreateGradientAtPoint(dF, x)
  gradientNorm = _CreateGradientNorm(gradient)
  inverseHessian = _CreateInverseHessianAtPoint(ddF, x)
  
  divergenceCounter = 0
  bestValue = 10**6
  while _IsGradientNormLarge(gradientNorm, epsilon):
  
    if _IsDiverging(x, F, bestValue, epsilon):
      divergenceCounter += 1
    else:
      bestValue = F(x._GetMatrixColumn(1))
    if divergenceCounter > 100:
      print "Divergence limit has been reached"
      break
      
    KMinimum = 1
    if useGolden == True:
      KStartingValue = (0, 1)
      direction = _CreateDescentDirection( inverseHessian * gradient )
      singleDimensionF = _CreateOneDimensionFunction(F, x, direction)
      
      KMinimum = GoldenSectionSearch(KStartingValue, singleDimensionF, epsilon, doUnimodal=True)
      
      x = _GoldenChangePoint(x, direction, KMinimum)
    else:
      x = _ChangePoint(x, inverseHessian, gradient, KMinimum)
      
    _PrintNewtonRaphson(gradientNorm, inverseHessian, x)
    
    gradient = _CreateGradientAtPoint(dF, x)
    gradientNorm = _CreateGradientNorm(gradient)
    inverseHessian = _CreateInverseHessianAtPoint(ddF, x)
      
  return x
  
def _MapToMathsNames(startingPoint, GoalFunction, FirstPartialDerivativeFunctions, HessianPartialDerivativeFunctions):
  """startingPoint is a Python list of numbers;
     GoalFunction is a function saved in a variable (higher order function);
     FirstPartialDerivativeFunctions is a Python list of functions;
     HessianPartialDerivativeFunctions is a Python list of lists of functions;"""
  x = _CreateColumnMatrix(startingPoint)
  F = GoalFunction
  dF = FirstPartialDerivativeFunctions
  ddF = HessianPartialDerivativeFunctions
  return x, F, dF, ddF
  
def _CreateColumnMatrix(list):
  columnMatrix = []
  for value in list:
    columnMatrix.append( [value] )
    
  return Matrix(columnMatrix)
    
def _CreateGradientAtPoint(dF, x):
  gradient = []
  for partialDerivativeFunction in dF:
    result = partialDerivativeFunction(x._GetMatrixColumn(1))
    gradient.append(  [result] )
    
  return Matrix(gradient)

def _CreateGradientNorm(gradient):
  sum = 0
  for partialDerivative in gradient._GetMatrixColumn(1):
    sum += partialDerivative**2
    
  return math.sqrt(sum)

def _CreateInverseHessianAtPoint(ddF, x):
  hessianValues = []
  for derivativeList in ddF:
    
    results = []
    for derivative in derivativeList:
      results.append(derivative(x._GetMatrixColumn(1)))
    hessianValues.append(results)
    
  hessianMatrix = Matrix(hessianValues)
  hessianMatrix.inverse()
  return hessianMatrix

def _IsGradientNormLarge(gradientNorm, epsilon):
  if epsilon < gradientNorm:
    return True
  return False

def _IsDiverging(x, F, bestValue, epsilon):
  x = x._GetMatrixColumn(1)
  if (bestValue - epsilon) <= F(x):
    return True
  return False
  
def _CreateDescentDirection(gradient):
  descentDirection = []
  gradientNorm = _CreateGradientNorm(gradient)
  for value in gradient._GetMatrixColumn(1):
    descentDirection.append( [value / ((-1) * gradientNorm)] )
    
  return Matrix(descentDirection)
  
def _CreateOneDimensionFunction(compositeFunction, KPoint, KVector):
  """baseF(x) = x[0]**2           + x[1]**2 is given KPoint = [1 2] and KVector = [3 4]
     compositeF(k) = (1 + 3*k)**2 + (2 + 4*k)**2 is the resulting function"""
  def interdictor(value):
    currentCompositePoint = []
    for i in range(len(KPoint._GetMatrixColumn(1))):
      currentCompositePoint.append(_KFunction(KPoint[i+1,1], KVector[i+1,1]*value))
    
    calculation = compositeFunction(currentCompositePoint)
    return calculation
    
  return interdictor
  
def _KFunction(a, b):
  return a + b 
  
def _GoldenChangePoint(x, direction, KMinimum):
  distance = direction.scale(KMinimum)
    
  return (x + distance)

def _ChangePoint(x, inverseHessian, gradient, KMinimum):
  distance = inverseHessian * gradient
  distance = distance.scale(KMinimum)
    
  return (x - distance)

def _PrintNewtonRaphson(gradientNorm, inverseHessianMatrix, x):
  print "-.-.-.-.-.-.-.-.-.-"
  print "gradientNorm:",
  print gradientNorm
  print "inverseHessianMatrix:",
  print inverseHessianMatrix
  print "x:",
  print x
  