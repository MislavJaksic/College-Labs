import Programs.CoordinateDescent
import Tasks.TaskFunctions

import pytest

def test_CoordinateDescent_IsAtLeastOnePointWasMovedT():
  x = [1,2,3,4]
  xPrevious = [1,2,3,5]
  epsilon = (0.1)**6
  assert Programs.CoordinateDescent._IsAtLeastOnePointWasMoved(x, xPrevious, epsilon) == True

def test_CoordinateDescent_IsAtLeastOnePointWasMovedF():
  x = [1,2,3,4]
  xPrevious = [1,2,3,4]
  epsilon = (0.1)**6
  assert Programs.CoordinateDescent._IsAtLeastOnePointWasMoved(x, xPrevious, epsilon) == False
  
def test_CoordinateDescent_CreateCompositePoint():
  x = [1,2,3,4]
  i = 2
  assert Programs.CoordinateDescent._CreateCompositePoint(x, i) == [1,2,"KFunction",4]
  
def test_CoordinateDescent_CreateOneDimensionFunction():
  compositeFunction = lambda x: x[0]**2 + x[1]**2 + x[2]**2
  compositePoint = [1,2,"KFunction"]
  KPoint = [3, 4]
  result = Programs.CoordinateDescent._CreateOneDimensionFunction(compositeFunction, compositePoint, 2, KPoint)
  assert result(5) == 534
  
def test_CoordinateDescent():
  startingPoint = [7,3]
  GoalFunction = lambda x: x[0]**2 + 4*x[1]**2
  result = Programs.CoordinateDescent.CoordinateDescent(startingPoint, GoalFunction)
  assert (-0.1 < result[0]) and (result[0] < 0.1) and (-0.1 < result[1]) and (result[1] < 0.1)