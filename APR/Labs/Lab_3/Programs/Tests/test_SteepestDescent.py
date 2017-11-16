import Programs.SteepestDescent
import Tasks.TaskFunctions

import pytest
  
def test_SteepestDescent_CalculateVectorNorm():
  gradient = [4, 5]
  result = Programs.SteepestDescent._CalculateVectorNorm(gradient)
  assert (6.3 < result) and (result < 6.5)
  
def test_SteepestDescent_CalculateGradientAtPoint():
  dF = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  x = [3, 5]
  assert Programs.SteepestDescent._CalculateGradientAtPoint(dF, x) == [-2, 24]
    
def test_SteepestDescent_CalculateDescentDirection():
  gradient = [-8, -16]
  result = Programs.SteepestDescent._CalculateDescentDirection(gradient)
  assert (0.4 < result[0]) and (result[0] < 0.5) and (0.8 < result[1]) and (result[1] < 0.9)
  
def test_SteepestDescentGolden():
  startingPoint = [0, 0]
  GoalFunction = Tasks.TaskFunctions.f2
  PartialDerivativeFunctions = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  result = Programs.SteepestDescent.SteepestDescent(startingPoint, GoalFunction, PartialDerivativeFunctions)
  assert (3.9 < result[0]) and (result[0] < 4.1) and (1.9 < result[1]) and (result[1] < 2.1)
  
def test_SteepestDescentNoGolden():
  startingPoint = [0, 0]
  GoalFunction = Tasks.TaskFunctions.f2
  PartialDerivativeFunctions = [Tasks.TaskFunctions.df2x0, Tasks.TaskFunctions.df2x1]
  result = Programs.SteepestDescent.SteepestDescent(startingPoint, GoalFunction, PartialDerivativeFunctions, useGolden=False)
  assert (3.9 < result[0]) and (result[0] < 4.1) and (1.1 < result[1]) and (result[1] < 1.3)