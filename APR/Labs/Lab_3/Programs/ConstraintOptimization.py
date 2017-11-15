from Helpers.Matrix import Matrix
from Helpers.SimplexNelderMead import SimplexNelderMead

import math

LARGE_VALUE = 10**6

def ConstraintOptimization(startingPoint, GoalFunction, Inequalities, Equalities, t=1, epsilon=(0.1)**6):
  x, F, gs, hs = _MapToMathsNames(startingPoint, GoalFunction, Inequalities, Equalities)
  
  x = _PlacePointWithinConstraints(x, gs)
  #print "Point is within constraints:"
  #print x
  
  divergenceCounter = 0
  bestValue = F(x)
  while (True):
    
    replacementF = _CreateReplacementFunction(F, gs, hs, t)
    newx = SimplexNelderMead(x, replacementF)
    
    #print newx
    
    if _IsDiverging(x, F, bestValue, epsilon):
      divergenceCounter += 1
    else:
      bestValue = F(x)
      
    if divergenceCounter > 100:
      print "Divergence limit has been reached"
      break
    if not _IsPointMoved(x, newx, epsilon):
      break
      
    x = newx
    t = t * 10

  return x
  
def _MapToMathsNames(startingPoint, GoalFunction, Inequalities, Equalities):
  """startingPoint is a Python list of numbers;
     GoalFunction is a function saved in a variable (higher order function);
     Inequalities is a Python list of functions;
     Equalities is a Python list of functions;"""
  x = startingPoint
  F = GoalFunction
  gs = Inequalities
  hs = Equalities
  return x, F, gs, hs

def _PlacePointWithinConstraints(x, gs):
  moveFunction = _CreateFunctionThatWillMovePoint(gs)
  
  replacementx = SimplexNelderMead(x, moveFunction)
  return replacementx
  
def _CreateFunctionThatWillMovePoint(gs):
  """G is the replacement function;
     G(x) = - ( SUM( g(x) )"""
  def interdictor(x):
    result = 0
    for g in gs:
      if _IsOutsideConstraint(g(x)):
        result -= g(x)
    if _IsNegative(result):
      return 0
      
    return result
    
  return interdictor
  
def _IsPointMoved(x, newx, epsilon):
  for i in range(len(x)):
    if math.fabs(x[i] - newx[i]) > epsilon:
      return True
  return False

def _IsDiverging(x, F, bestValue, epsilon):
  if (bestValue - epsilon) <= F(x):
    return True
  return False
  
def _CreateReplacementFunction(F, gs, hs, t):
  """U is the replacement function;
     U(x, t) = F(x) - ( SUM( ln(g(x)) ) / t ) + t * ( SUM( h(x)**2 ) )"""
  def interdictor(x):
    result = F(x)
    for g in gs:
      if _IsOutsideConstraint(g(x)):
        return LARGE_VALUE
      else:
        result -= math.log(g(x)) / float(t)
    for h in hs:
      result += t * (h(x)**2)
      
    return result
    
  return interdictor
  
def _IsOutsideConstraint(x):
  if (x < 0):
    return True
  return False
  
def _IsNegative(x):
  if (x < 0):
    return True
  return False
