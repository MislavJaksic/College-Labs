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
  
  simplex = CreateSimplex(x0, steps)
  print "centroid     F(centroid)"
  centroid = simplex[0] #for the purposes of the while condition
  
  while not IsSimplexOverMin(simplex, centroid, F, epsilon):
    bestIndex, worstIndex = GetBestAndWorstSimplexIndexes(simplex, F)
    
    centroid = GetSimplexCentroid(simplex, worstIndex, F)
    
    PrintCentroid(centroid, F)
    
    xRefl = ReflectWorseOverCentroid(simplex, worstIndex, centroid, alpha)
    
    if IsPointBetterThenAnother(xRefl, simplex[bestIndex], F):
      xExpa = ExpendReflectedOverCentroid(xRefl, centroid, gamma)
      
      if IsPointBetterThenAnother(xExpa, simplex[bestIndex], F):
        simplex[worstIndex] = xExpa
      else:
        simplex[worstIndex] = xRefl
    
    else:
      if IsEverySimplexPointBetterThenReflectedPoint(xRefl, simplex, worstIndex, F):
        if IsPointBetterThenAnother(xRefl, simplex[worstIndex], F):
          simplex[worstIndex] = xRefl
          
        xCont = ContractPoint(simplex, worstIndex, centroid, beta)
        if IsPointBetterThenAnother(xCont, simplex[worstIndex], F):
          simplex[worstIndex] = xCont
        else:
          simplex = MoveTowardsBest(simplex, bestIndex, sigma)
      else:
        simplex[worstIndex] = xRefl
        
  return simplex[bestIndex]
      
def CreateSimplex(x0, steps):
  """If x0=[1,2,3] and steps=[4,5,6]:
     simplex=[[1,2,3],[5,2,3],[1,7,3],[1,2,9]]"""
  simplex = []
  simplex.append(x0)
  for i in range(len(x0)):
    simplexPoint = copy(x0)
    simplexPoint[i] += steps[i]
    simplex.append(simplexPoint)
  return simplex
  
def IsSimplexOverMin(simplex, centroid, F, epsilon):
  quadraticSum = 0
  centroidDistance = F(centroid)
  for x in simplex:
    quadraticSum += (F(x) - centroidDistance)**2
  quadraticSum /= float(len(simplex)) 
  if sqrt(quadraticSum) <= epsilon:
    return True
  return False
  
def GetBestAndWorstSimplexIndexes(simplex, F):
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

def GetSimplexCentroid(simplex, worstIndex, F):
  centroid = []
  for j in range(len(simplex[0])):
    sum = 0
    for i in range(len(simplex)):
      if i == worstIndex:
        continue
      sum += simplex[i][j]
    centroid.append(sum / float(len(simplex) - 1))
  return centroid

def PrintCentroid(centroid, F):
  row = ""
  row += str(centroid)
  row += " "
  row += str(F(centroid))
  print row

def ReflectWorseOverCentroid(simplex, worstIndex, centroid, alpha):
  reflectedPoint = []
  for i in range(len(simplex[0])):
    coord = (1 + alpha)*centroid[i] - alpha*simplex[worstIndex][i]
    reflectedPoint.append(coord)
  
  return reflectedPoint
  
def ExpendReflectedOverCentroid(xRefl, centroid, gamma):
  expandedPoint = []
  for i in range(len(xRefl)):
    coord = (1 - gamma)*centroid[i] + gamma*xRefl[i]
    expandedPoint.append(coord)
  
  return expandedPoint
  
def IsPointBetterThenAnother(onePoint, twoPoint, F):
  if F(onePoint) < F(twoPoint):
    return True
  return False
    
def IsEverySimplexPointBetterThenReflectedPoint(xRefl, simplex, worstIndex, F):
  for i in range(len(simplex)):
    if i == worstIndex:
      continue
    if IsPointBetterThenAnother(simplex[i], xRefl, F): #check the condition here!!!
      return False
  return True
  
def ContractPoint(simplex, worstIndex, centroid, beta):
  contractedPoint = []
  for i in range(len(simplex[0])):
    coord = (1 - beta)*centroid[i] + beta*simplex[worstIndex][i]
    contractedPoint.append(coord)
  
  return contractedPoint
  
def MoveTowardsBest(simplex, bestIndex, sigma):
  bestPoint = copy(simplex[bestIndex])
  for x in simplex:
    for i in range(len(simplex[0])):
      x[i] = sigma*(x[i] + bestPoint[i])
      
  return simplex
  