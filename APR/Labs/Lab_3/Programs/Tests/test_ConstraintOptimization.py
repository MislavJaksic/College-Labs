import Programs.ConstraintOptimization
import Tasks.TaskFunctions
from Programs.Helpers.Matrix import Matrix

import pytest
from copy import copy
  
def test_ConstraintOptimization_IsPointMoved():
  x = [1, 2, 3]
  newx = [1, 2, 4]
  epsilon = 0.5
  assert Programs.ConstraintOptimization._IsPointMoved(x, newx, epsilon) == True
  
def test_ConstraintOptimization_CreateReplacementFunction():
  F = Tasks.TaskFunctions.f2
  gs = [Tasks.TaskFunctions.constraint1, Tasks.TaskFunctions.constraint2]
  hs = []
  t = 1
  replacementF = Programs.ConstraintOptimization._CreateReplacementFunction(F, gs, hs, t)
  x = [1, 2]
  assert replacementF(x) == 9
  
def test_ConstraintOptimization():
  startingPoint = [200, 200]
  GoalFunction = Tasks.TaskFunctions.f2
  Inequalities = [Tasks.TaskFunctions.constraint1, Tasks.TaskFunctions.constraint2, Tasks.TaskFunctions.constraint6, Tasks.TaskFunctions.constraint7, Tasks.TaskFunctions.constraint8, Tasks.TaskFunctions.constraint9]
  Equalities = []
  
  result = Programs.ConstraintOptimization.ConstraintOptimization(startingPoint, GoalFunction, Inequalities, Equalities)
  assert (1.9 < result[0]) and (result[0] < 2.1) and (1.9 < result[1]) and (result[1] < 2.1)