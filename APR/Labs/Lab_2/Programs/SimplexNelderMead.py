from copy import copy
from math import sqrt

def SimplexNelderMead(startingPoint, GoalFunction, alpha=1, beta=0.5, gamma=2, sigma=0.5, steps=[], epsilon=(0.1)**6):
  """Reflection, expansion, contraction and moving all points"""
  x0 = startingPoint
  reflCoef = alpha
  expaCoef = beta
  contCoef = gamma
  moveCoef = sigma
  F = GoalFunction
  if not steps:
    for i in range(len(x0)):
      steps.append(1)
  
  simplex = _CreateSimplex(x0, steps)
  centroid = simplex[0]
  
  print "centroid     F(centroid)"
  
  while not _IsSimplexOverMin(simplex, centroid, F, epsilon):
    bestIndex, worstIndex = _GetBestAndWorstSimplexIndexes(simplex, F)
    
    centroid = _GetSimplexCentroid(simplex, worstIndex, F)
    
    _PrintCentroid(centroid, F) #Deactivate during peformance analysis
    
    xRefl = _ReflectWorseOverCentroid(simplex, worstIndex, centroid, alpha)
    
    if _IsPointBetterThenAnother(xRefl, simplex[bestIndex], F):
      xExpa = _ExpendReflectedOverCentroid(xRefl, centroid, gamma)
      
      if _IsPointBetterThenAnother(xExpa, simplex[bestIndex], F):
        simplex[worstIndex] = xExpa
      else:
        simplex[worstIndex] = xRefl
    
    else:
      if _IsEverySimplexPointBetterThenReflectedPoint(xRefl, simplex, worstIndex, F):
        if _IsPointBetterThenAnother(xRefl, simplex[worstIndex], F):
          simplex[worstIndex] = xRefl
          
        xCont = _ContractPoint(simplex, worstIndex, centroid, beta)
        if _IsPointBetterThenAnother(xCont, simplex[worstIndex], F):
          simplex[worstIndex] = xCont
        else:
          simplex = _MoveTowardsBest(simplex, bestIndex, sigma)
      
      else:
        simplex[worstIndex] = xRefl
        
  return simplex[bestIndex]
      
def _CreateSimplex(x0, steps):
  """If x0=[1,2,3] and steps=[4,5,6]:
     simplex=[[1,2,3],[1+4,2,3],[1,2+5,3],[1,2,3+6]]"""
  simplex = []
  simplex.append(x0)
  for i in range(len(x0)):
    simplexPoint = copy(x0)
    simplexPoint[i] += steps[i]
    simplex.append(simplexPoint)
  return simplex
  
def _IsSimplexOverMin(simplex, centroid, F, epsilon):
  quadraticSum = 0
  centroidDistance = F(centroid)
  for x in simplex:
    quadraticSum += (F(x) - centroidDistance)**2
  quadraticSum = quadraticSum / float(len(simplex))
  
  if sqrt(quadraticSum) <= epsilon:
    return True
  return False
  
def _GetBestAndWorstSimplexIndexes(simplex, F):
  bestIndex = 0
  worstIndex = 0
  
  for index in range(len(simplex)):
    bestPointDistance = F(simplex[bestIndex])
    worstPointDistance = F(simplex[worstIndex])
    pointDistance = F(simplex[index])
    
    if pointDistance < bestPointDistance:
      bestIndex = index
    if pointDistance > worstPointDistance:
      worstIndex = index
      
  return bestIndex, worstIndex

def _GetSimplexCentroid(simplex, worstIndex, F):
  centroid = []
  for j in range(len(simplex[0])):
    sum = 0
    for i in range(len(simplex)):
      if i == worstIndex:
        continue
      sum += simplex[i][j]
    centroid.append(sum / float(len(simplex) - 1))
  return centroid

def _PrintCentroid(centroid, F):
  row = ""
  row += str(centroid)
  row += " "
  row += str(F(centroid))
  print row

def _ReflectWorseOverCentroid(simplex, worstIndex, centroid, alpha):
  reflectedPoint = []
  for i in range(len(simplex[0])):
    coord = (1 + alpha)*centroid[i] - alpha*simplex[worstIndex][i]
    reflectedPoint.append(coord)
  
  return reflectedPoint
  
def _ExpendReflectedOverCentroid(xRefl, centroid, gamma):
  expandedPoint = []
  for i in range(len(xRefl)):
    coord = (1 - gamma)*centroid[i] + gamma*xRefl[i]
    expandedPoint.append(coord)
  
  return expandedPoint
  
def _IsPointBetterThenAnother(onePoint, twoPoint, F):
  if F(onePoint) < F(twoPoint):
    return True
  return False
    
def _IsEverySimplexPointBetterThenReflectedPoint(xRefl, simplex, worstIndex, F):
  for i in range(len(simplex)):
    if i == worstIndex:
      continue
    if _IsPointBetterThenAnother(xRefl, simplex[i], F):
      return False
  return True
  
def _ContractPoint(simplex, worstIndex, centroid, beta):
  contractedPoint = []
  for i in range(len(simplex[0])):
    coord = (1 - beta)*centroid[i] + beta*simplex[worstIndex][i]
    contractedPoint.append(coord)
  
  return contractedPoint
  
def _MoveTowardsBest(simplex, bestIndex, sigma):
  bestPoint = copy(simplex[bestIndex])
  for x in simplex:
    for i in range(len(simplex[0])):
      x[i] = sigma*(x[i] + bestPoint[i])
      
  return simplex
  