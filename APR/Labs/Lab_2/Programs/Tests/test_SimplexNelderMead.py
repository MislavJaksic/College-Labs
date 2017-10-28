import Programs.SimplexNelderMead
import Tasks.TaskFunctions

import pytest

def test_SimplexNelderMead_CreateSimplex():
  x0 =[0,0,0]
  steps = [1,1,1]
  assert Programs.SimplexNelderMead._CreateSimplex(x0, steps) == [[0,0,0],[1,0,0],[0,1,0],[0,0,1]]
  
def test_SimplexNelderMead_GetBestAndWorstSimplexIndexes():
  simplex = [[1,0],[0,2],[0,0]]
  F = Tasks.TaskFunctions.f1
  assert Programs.SimplexNelderMead._GetBestAndWorstSimplexIndexes(simplex, F) == (2,1)

def test_SimplexNelderMead_GetSimplexCentroid():
  simplex = [[1,2,3],[0,2,4],[-2,0,3],[-4,0,1]]
  worstIndex = 1
  F = lambda x: (x[1]**2) + (x[2]**2) + (x[3]**2)
  resultCentroid = [-5/3., 2/3., 7/3.]
  assert Programs.SimplexNelderMead._GetSimplexCentroid(simplex, worstIndex, F) == resultCentroid

def test_SimplexNelderMead_ReflectWorseOverCentroid():
  simplex = [[1,2,3],[0,2,4],[-2,0,3],[-4,0,1]]
  worstIndex = 1
  alpha = 1
  centroid = [-5/3., 2/3., 7/3.]
  
  result = Programs.SimplexNelderMead._ReflectWorseOverCentroid(simplex, worstIndex, centroid, alpha)
  
  assert (-11/3. < result[0]) and (result[0] < -9/3.) and (-3/3.< result[1]) and (result[1] < -1/3.) and (1/3. < result[2]) and (result[2] < 3/3.)

def test_SimplexNelderMead_ExpendReflectedOverCentroid():
  xRefl = [-10/3., -2/3., 2/3.]
  gamma = 2
  centroid = [-5/3., 2/3., 7/3.]
  
  result = Programs.SimplexNelderMead._ExpendReflectedOverCentroid(xRefl, centroid, gamma)
  
  assert (-5.1 < result[0]) and (result[0] < -4.9) and (-2.1 < result[1]) and (result[1] < -1.9) and (-1.1 < result[2]) and (result[2] < -0.9)

def test_SimplexNelderMead():
  startingPoint = [5,5]
  GoalFunction = lambda x: x[0]**2 + x[1]**2
  
  result = Programs.SimplexNelderMead.SimplexNelderMead(startingPoint, GoalFunction)
  assert (-0.1 < result[0]) and (result[0] < 0.1) and (-0.1 < result[1]) and (result[1] < 0.1)