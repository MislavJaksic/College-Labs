from Helpers.UnimodalGolden import GoldenSectionSearch
from Helpers.Matrix import Matrix

import math

DEFAULT_K_VALUE = 1
DIVERGENCE_THRESHOLD = 100

def NewtonRaphson(startingPoint, GoalFunction, PartialDerivativeFunctions, HessianPartialDerivativeFunctions, useGolden=True, epsilon=((0.1)**6)):
  x, F, dF, ddF = _MapToMathsNames(startingPoint, GoalFunction, PartialDerivativeFunctions, HessianPartialDerivativeFunctions)
  
  divergenceCounter = 0
  bestValue = F(x._GetMatrixColumn(1))
  while (True):
    
    gradient = _CalculateGradientAtPoint(dF, x)
    gradientNorm = _CalculateVectorNorm(gradient)
    inverseHessian = _CalculateInverseHessianAtPoint(ddF, x)
    
    moveDirection = _CalculateMoveDirection(inverseHessian * gradient, useGolden)
    
    KMin = _FindOptimumStepConstant(F, x, moveDirection, useGolden, epsilon)
    
    x = _MovePoint(x, KMin, moveDirection)
      
    _PrintNewtonRaphson(gradientNorm, inverseHessian, x)
    
    if _IsDiverging(x, F, bestValue, epsilon):
      divergenceCounter += 1
    else:
      bestValue = F(x._GetMatrixColumn(1))
      
    if divergenceCounter > DIVERGENCE_THRESHOLD:
      print "Divergence limit has been reached"
      break
    if _IsGradientNormSmall(gradientNorm, epsilon):
      break
      
  return x._GetMatrixColumn(1)
  
def _MapToMathsNames(startingPoint, GoalFunction, PartialDerivativeFunctions, HessianPartialDerivativeFunctions):
  """startingPoint is a Python list of numbers;
     GoalFunction is a function saved in a variable (higher order function);
     PartialDerivativeFunctions is a Python list of functions;
     HessianPartialDerivativeFunctions is a Python list of lists of functions;"""
  x = _CreateColumnMatrix(startingPoint)
  F = GoalFunction
  dF = PartialDerivativeFunctions
  ddF = HessianPartialDerivativeFunctions
  return x, F, dF, ddF
  
def _CreateColumnMatrix(list):
  columnMatrix = []
  for value in list:
    columnMatrix.append( [value] )
    
  return Matrix(columnMatrix)
    
def _CalculateGradientAtPoint(dF, x):
  gradient = []
  for partialDerivativeFunction in dF:
    result = partialDerivativeFunction(x._GetMatrixColumn(1))
    gradient.append(  [result] )
    
  return Matrix(gradient)

def _CalculateVectorNorm(vector):
  sum = 0
  for compoenent in vector._GetMatrixColumn(1):
    sum += compoenent**2
    
  return math.sqrt(sum)

def _CalculateInverseHessianAtPoint(ddF, x):
  hessianValues = []
  for derivativeList in ddF:
    
    results = []
    for derivative in derivativeList:
      results.append(derivative(x._GetMatrixColumn(1)))
    hessianValues.append(results)
    
  hessianMatrix = Matrix(hessianValues)
  hessianMatrix.inverse()
  return hessianMatrix

def _CalculateMoveDirection(gradient, useGolden):
  if useGolden == True:
    descentDirection = []
    gradientNorm = _CalculateVectorNorm(gradient)
    for value in gradient._GetMatrixColumn(1):
      descentDirection.append( [value / gradientNorm] )
      
    return Matrix(descentDirection)
  else:
    return gradient
  
def _FindOptimumStepConstant(F, x, moveDirection, useGolden, epsilon):
  if useGolden == True:
    KMin = _FindKMinimum(F, x, moveDirection, epsilon)
  else:
    KMin = DEFAULT_K_VALUE
    
  return KMin
  
def _FindKMinimum(F, x, moveDirection, epsilon):
  KStartingValue = (0, 1)
  singleDimensionF = _CreateOneDimensionFunction(F, x, moveDirection)
  
  KMinimum = GoldenSectionSearch(KStartingValue, singleDimensionF, epsilon, doUnimodal=True)
  return KMinimum
  
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
  
def _IsGradientNormSmall(gradientNorm, epsilon):
  if epsilon > gradientNorm:
    return True
  return False

def _IsDiverging(x, F, bestValue, epsilon):
  x = x._GetMatrixColumn(1)
  if (bestValue - epsilon) <= F(x):
    return True
  return False
  
def _MovePoint(x, KMin, direction):
  distance = direction.scale(KMin)
  if KMin == DEFAULT_K_VALUE:
    return (x - distance)
  return (x + distance)

def _PrintNewtonRaphson(gradientNorm, inverseHessianMatrix, x):
  print "-.-.-.-.-.-.-.-.-.-"
  print "gradientNorm:",
  print gradientNorm
  print "inverseHessianMatrix:",
  print inverseHessianMatrix
  print "x:",
  print x
  