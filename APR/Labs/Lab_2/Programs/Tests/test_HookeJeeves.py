import Programs.HookeJeeves
import Tasks.TaskFunctions

import pytest

def test_HookeJeeves_CalculateStepPoint():
  x = [1,2,3,4]
  step = 1
  coordinate = 0
  assert Programs.HookeJeeves._CalculateStepPoint(x, step, coordinate) == [2,2,3,4]

def test_HookeJeeves_FindBestStepPointOnf1():
  xp = [5,5]
  steps = [1,1]
  GoalFunction = Tasks.TaskFunctions.f1
  assert Programs.HookeJeeves._FindBestStepPoint(xp, steps, GoalFunction) == [4,6]
  
def test_HookeJeeves_FindBestStepPointOnTrivialf():
  xp = [5,5]
  steps = [1,1]
  GoalFunction = lambda x: x[0]**2 + x[1]**2
  assert Programs.HookeJeeves._FindBestStepPoint(xp, steps, GoalFunction) == [4,4]
  
def test_HookeJeeves_IsXBFartherFromMinThenXN():
  xb = [5,5]
  xn = [4,4]
  GoalFunction = lambda x: x[0]**2 + x[1]**2
  assert Programs.HookeJeeves._IsXBFartherFromMinThenXN(xb, xn, GoalFunction) == True
  
def test_HookeJeeves_ReflectXBAccrossXN():
  xb = [5,4]
  xn = [3,2]
  assert Programs.HookeJeeves._ReflectXBAccrossXN(xb, xn) == [1,0]
  
def test_HookeJeeves_HalveSteps():
  steps = [1,1]
  assert Programs.HookeJeeves._HalveSteps(steps) == [0.5,0.5]
  
def test_HookeJeeves():
  startingPoints = [7,3]
  steps = [1,1]
  GoalFunction = lambda x: x[0]**2 + 4*x[1]**2
  assert Programs.HookeJeeves.HookeJeeves(startingPoints, GoalFunction, steps=steps) == [0,0]
  