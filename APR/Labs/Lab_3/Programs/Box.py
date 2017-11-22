from Helpers.SimplexNelderMead import SimplexNelderMead

from copy import copy
from math import sqrt
from random import random

DIVERGENCE_THRESHOLD = 100
LARGE_VALUE = 10**6

def Box(startingPoint, GoalFunction, Inequalities, Interval, alpha=1.3, epsilon=(0.1)**6):
  x, F, gs, lowBarrier, highBarrier = _MapToMathsNames(startingPoint, GoalFunction, Inequalities, Interval)
  
  x = _PlacePointWithinConstraints(x, gs)
  
  box, centroid = _CreateBoxAndCentroid(x, gs, lowBarrier, highBarrier)
  
  noImprovementCounter = 0
  bestFValue = LARGE_VALUE
  while not _IsBoxOverMin(box, centroid, F, epsilon):
    firstWorstIndex, secondWorstIndex = _GetFirstAndSecondWorstBoxIndexes(box, F)
    
    centroid = _CreateBoxCentroid(box, firstWorstIndex=firstWorstIndex)
    
    xRefl = _ReflectWorseOverCentroid(box, firstWorstIndex, centroid, alpha)
    
    for coordinateCounter in range(len(xRefl)):
      if xRefl[coordinateCounter] < lowBarrier:
        xRefl[coordinateCounter] = lowBarrier
      elif xRefl[coordinateCounter] > highBarrier:
        xRefl[coordinateCounter] = highBarrier
        
    xRefl = _PlaceBoxPointWithinConstraints(xRefl, centroid, gs)
    
    if _IsPointBetterThenAnother(box[secondWorstIndex], xRefl, F):
      for coordinate in range(len(xRefl)):
        xRefl[coordinate] = 0.5 * (xRefl[coordinate] + centroid[coordinate])
    
    box[firstWorstIndex] = xRefl
    
    if _IsDiverging(x, F, bestFValue, epsilon):
      noImprovementCounter += 1
    else:
      bestFValue = F(x)
      
    if (noImprovementCounter > DIVERGENCE_THRESHOLD):
      print "Divergence limit has been reached. Goal function hasn't improved for " + str(DIVERGENCE_THRESHOLD) + " iterations." 
      break
      
  return centroid
      
def _MapToMathsNames(startingPoint, GoalFunction, Inequalities, Interval):
  """startingPoint is a Python list of numbers;
     GoalFunction is a function saved in a variable (higher order function);
     Inequalities is a Python list of functions;"""
  x = startingPoint
  F = GoalFunction
  gs = Inequalities
  lowBarrier = Interval[0]
  highBarrier = Interval[1]
  return x, F, gs, lowBarrier, highBarrier
  
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
  
def _IsOutsideConstraint(x):
  if (x < 0):
    return True
  return False
  
def _IsNegative(x):
  if (x < 0):
    return True
  return False
  
def _CreateBoxAndCentroid(x, gs, lowBarrier, highBarrier):
  """"""
  centroid = x
  box = []
  for pointCounter in range(2*len(x)):
    
    point = []
    for coordinateCounter in range(len(x)):
      coordinate = lowBarrier + random()*(highBarrier - lowBarrier)
      point.append(coordinate)
    
    point = _PlaceBoxPointWithinConstraints(point, centroid, gs)
    box.append(point)
    
    centroid = _CreateBoxCentroid(box)
  
  return box, centroid
  
def _PlaceBoxPointWithinConstraints(point, centroid, gs):
  while (_IsPointOutsideConstraints(point, gs)):
    for coordinate in range(len(point)):
      point[coordinate] = 0.5 * (point[coordinate] + centroid[coordinate])
  
  return point
    
def _IsPointOutsideConstraints(point, gs):
  for g in gs:
    if (g(point) < 0):
      return True
  return False 
    
def _CreateBoxCentroid(box, firstWorstIndex=(-1)):
  centroid = []
  for coordinateCounter in range(len(box[0])):
  
    sum = 0
    for pointCounter in range(len(box)):
      if pointCounter == firstWorstIndex:
        continue
      sum += box[pointCounter][coordinateCounter]
      
    if (firstWorstIndex != (-1)):
      centroid.append(sum / float(len(box) - 1))
    else:
      centroid.append(sum / float(len(box)))
    
  return centroid
  
def _IsBoxOverMin(box, centroid, F, epsilon):
  quadraticSum = 0
  centroidDistance = F(centroid)
  for x in box:
    quadraticSum += (F(x) - centroidDistance)**2
  quadraticSum = quadraticSum / float(len(box))
  
  print "error: ",
  print sqrt(quadraticSum)
  if sqrt(quadraticSum) <= epsilon:
    return True
  return False
  
def _GetFirstAndSecondWorstBoxIndexes(box, F):
  firstWorstIndex = 0
  secondWorstIndex = 0
  firstWorstPointDistance = F(box[firstWorstIndex])
  secondWorstPointDistance = F(box[secondWorstIndex])
  
  for index in range(len(box)):
    pointDistance = F(box[index])
    
    if pointDistance > firstWorstPointDistance:
      secondWorstIndex = firstWorstIndex
      firstWorstIndex = index
      
      secondWorstPointDistance = firstWorstPointDistance
      firstWorstPointDistance = pointDistance
      
    elif pointDistance > secondWorstPointDistance:
      secondWorstIndex = index
      secondWorstPointDistance = pointDistance
      
  return firstWorstIndex, secondWorstIndex

def _ReflectWorseOverCentroid(box, firstWorstIndex, centroid, alpha):
  reflectedPoint = []
  for i in range(len(box[0])):
    coord = (1 + alpha)*centroid[i] - alpha*box[firstWorstIndex][i]
    reflectedPoint.append(coord)
  
  return reflectedPoint
  
def _IsPointBetterThenAnother(onePoint, twoPoint, F):
  if F(onePoint) < F(twoPoint):
    return True
  return False
  
def _IsDiverging(x, F, bestFValue, epsilon):
  if (bestFValue - epsilon) <= F(x):
    return True
  return False
    