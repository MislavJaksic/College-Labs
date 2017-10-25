import Programs.HookeJeeves
import Tasks.TaskFunctions

import pytest

def test_HookeJeevesCalculateStepPoint():
  x = [1,2,3,4]
  step = 1
  coordinate = 0
  assert Programs.HookeJeeves.CalculateStepPoint(x, step, coordinate) == [2,2,3,4]

def test_HookeJeevesFindBestStepPointOnf1():
  xp = [5,5]
  steps = [1,1]
  GoalFunction = Tasks.TaskFunctions.f1
  assert Programs.HookeJeeves.FindBestStepPoint(xp, steps, GoalFunction) == [4,6]
  
def test_HookeJeevesFindBestStepPointOnTrivialf():
  xp = [5,5]
  steps = [1,1]
  GoalFunction = lambda x: x[0]**2 + x[1]**2
  assert Programs.HookeJeeves.FindBestStepPoint(xp, steps, GoalFunction) == [4,4]
  
def test_HookeJeevesIsXBFartherFromMinThenXN():
  xb = [5,5]
  xn = [4,4]
  GoalFunction = lambda x: x[0]**2 + x[1]**2
  assert Programs.HookeJeeves.IsXBFartherFromMinThenXN(xb, xn, GoalFunction) == True
  
def test_HookeJeevesReflectXBAccrossXN():
  xb = [5,4]
  xn = [3,2]
  assert Programs.HookeJeeves.ReflectXBAccrossXN(xb, xn) == [1,0]
  
def test_HookeJeevesHalveSteps():
  steps = [1,1]
  assert Programs.HookeJeeves.HalveSteps(steps) == [0.5,0.5]
  
def test_HookeJeeves():
  startingPoints = [7,3]
  steps = [1,1]
  GoalFunction = lambda x: x[0]**2 + 4*x[1]**2
  assert Programs.HookeJeeves.HookeJeeves(startingPoints, steps, GoalFunction) == [0,0]
  