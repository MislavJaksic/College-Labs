import Programs.Box
import Tasks.TaskFunctions

import pytest
from copy import copy
  
def test_Box_CreateBoxAndCentroid():
  x = [1, 2, 3, 4, 5]
  gs = [Tasks.TaskFunctions.constraint1, Tasks.TaskFunctions.constraint2]
  lowBarrier = -100
  highBarrier = 100
  
  box, centroid = Programs.Box._CreateBoxAndCentroid(x, gs, lowBarrier, highBarrier)
  assert len(box) == 10
  
def test_Box_PlaceBoxPointWithinConstraints():
  point = [10, 20]
  centroid = [2, 2]
  gs = [Tasks.TaskFunctions.constraint1, Tasks.TaskFunctions.constraint2]
  
  result = Programs.Box._PlaceBoxPointWithinConstraints(point, centroid, gs)
  assert (1.9 < result[0]) and (result[0] < 2.1) and (1.9 < result[1]) and (result[1] < 2.1)
  
def test_Box_IsPointOutsideConstraints():
  pointTrue = [10, 20]
  pointFalse = [1, 10]
  gs = [Tasks.TaskFunctions.constraint1, Tasks.TaskFunctions.constraint2]
  
  assert Programs.Box._IsPointOutsideConstraints(pointTrue, gs) == True
  assert Programs.Box._IsPointOutsideConstraints(pointFalse, gs) == False
  
def test_Box_CreateBoxCentroid():
  box = [[1,2,3],[0,2,4],[-2,0,3],[-4,0,1]]
  resultCentroid = [-5/4., 4/4., 11/4.]
  
  assert Programs.Box._CreateBoxCentroid(box) == resultCentroid
  
def test_Box_GetFirstAndSecondWorstBoxIndexes():
  box = [[100, 2],[200, 2],[400, 2],[300, 2], [500, 2]]
  F = Tasks.TaskFunctions.f2
  
  assert Programs.Box._GetFirstAndSecondWorstBoxIndexes(box, F) == (4, 2)
  
def test_Box():
  startingPoint = [200, 200]
  GoalFunction = Tasks.TaskFunctions.f2
  Inequalities = [Tasks.TaskFunctions.constraint1, Tasks.TaskFunctions.constraint2]
  Interval = [-100, 100]
  
  result = Programs.Box.Box(startingPoint, GoalFunction, Inequalities, Interval)
  assert (1.9 < result[0]) and (result[0] < 2.1) and (1.9 < result[1]) and (result[1] < 2.1)