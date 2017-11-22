from Helpers.UnimodalGolden import GoldenSectionSearch

import math

LARGE_VALUE = 10**6
DEFAULT_K_VALUE = 1
DIVERGENCE_THRESHOLD = 100

def SteepestDescent(startingPoint, GoalFunction, PartialDerivativeFunctions, useGolden=True, epsilon=((0.1)**6)):
  x, F, dF = _MapToMathsNames(startingPoint, GoalFunction, PartialDerivativeFunctions)
  
  noImprovementCounter = 0
  bestFValue = LARGE_VALUE
  print "direction     x        gradientNorm Kmin"
  while (True):
    gradient = _CalculateGradientAtPoint(dF, x)
    gradientNorm = _CalculateVectorNorm(gradient)
    descentDirection = _CalculateDescentDirection(gradient)

    KMin = _FindOptimumStepConstant(F, x, descentDirection, useGolden, epsilon)
    
    _PrintDescent(gradientNorm, descentDirection, x, KMin)
      
    x = _MovePoint(x, KMin, descentDirection)
    
    if _IsDiverging(x, F, bestFValue, epsilon):
      noImprovementCounter += 1
    else:
      bestFValue = F(x)
      
    if (noImprovementCounter > DIVERGENCE_THRESHOLD):
      print "Divergence limit has been reached. Goal function hasn't improved for " + str(DIVERGENCE_THRESHOLD) + " iterations." 
      break
    if _IsGradientNormSmall(gradientNorm, epsilon):
      break
      
  return x

def _MapToMathsNames(startingPoint, GoalFunction, PartialDerivativeFunctions):
  """startingPoint is a Python list of numbers;
     GoalFunction is a function saved in a variable (higher order function);
     PartialDerivativeFunctions is a list of function;"""
  x = startingPoint
  F = GoalFunction
  dF = PartialDerivativeFunctions
  return x, F, dF
    
def _CalculateGradientAtPoint(dF, x):
  """Gradient is the direction in which F increases the fastest"""
  gradient = []
  for partialDerivativeFunction in dF:
    result = partialDerivativeFunction(x)
    gradient.append(result)
    
  return gradient
  
def _CalculateVectorNorm(vector):
  """Vector norm = sqrt(component**2 + componenet2**2, ...)"""
  sum = 0
  for component in vector:
    sum += component**2
    
  return math.sqrt(sum)
    
def _CalculateDescentDirection(gradient):
  direction = _CalculateVectorDirection(gradient)
  descentDirection = _ChangeSign(direction)
  return descentDirection
  
def _CalculateVectorDirection(vector):
  direction = []
  vectorNorm = _CalculateVectorNorm(vector)
  for value in vector:
    direction.append(value / vectorNorm)
    
  return direction

def _ChangeSign(list):
  oppositeList = []
  for value in list:
    oppositeList.append((-1) * value)
    
  return oppositeList
 
def _FindOptimumStepConstant(F, x, descentDirection, useGolden, epsilon):
  if useGolden == True:
    KMin = _FindKMinimum(F, x, descentDirection, epsilon)
  else:
    KMin = DEFAULT_K_VALUE
    
  return KMin

def _MovePoint(x, KMin, descentDirection):
  for i in range(len(x)):
    x[i] = x[i] + KMin * descentDirection[i]
    
  return x
  
def _IsGradientNormSmall(gradientNorm, epsilon):
  if epsilon > gradientNorm:
    return True
  return False
  
def _IsDiverging(x, F, bestFValue, epsilon):
  if (bestFValue - epsilon) <= F(x):
    return True
  return False
  
def _FindKMinimum(F, x, descentDirection, epsilon):
  KStartingValue = (0, 1)
  singleDimensionF = _CreateOneDimensionFunction(F, x, descentDirection)
  
  KMinimum = GoldenSectionSearch(KStartingValue, singleDimensionF, epsilon, doUnimodal=True)
  return KMinimum
  
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
  
def _PrintDescent(gradientNorm, direction, x, KMin):
  for value in direction:
    print "{:+.2f} ".format(value),
  for value in x:
    print "{:+.2f} ".format(value),
    
  print "{:+.2f} ".format(gradientNorm),
  print "{:+.2f} ".format(KMin)