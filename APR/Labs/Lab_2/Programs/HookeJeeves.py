from copy import copy

def HookeJeeves(startingPoints, steps, GoalFunction, epsilon=0.25):
  """"""
  xb = xp = xn = []
  xb = xp = startingPoints
  print "xb     xp     xn     condition     steps[0]"
  
  while(steps[0] > epsilon):
    xn = FindBestStepPoint(xp, steps, GoalFunction)
    PrintRow(xb, xp, xn, steps[0])
    
    if IsXBFartherFromMinThenXN(xb, xn, GoalFunction):
      xp = ReflectXBAccrossXN(xb, xn)
      xb = xn
    else:
      steps = HalveSteps(steps)
      xp = xb
      
  return xb
     
def FindBestStepPoint(xp, steps, GoalFunction):
  bestPoint = copy(xp)
  for i in range(len(bestPoint)): 
    plusPoint = CalculateStepPoint(bestPoint,       steps[i], i)
    zeroPoint = CalculateStepPoint(bestPoint,              0, i)
    minusPoint = CalculateStepPoint(bestPoint, (-1)*steps[i], i)
    # print plusPoint
    # print zeroPoint
    # print minusPoint
    
    # print GoalFunction(plusPoint)
    # print GoalFunction(zeroPoint)
    # print GoalFunction(minusPoint)
    if GoalFunction(minusPoint) < GoalFunction(zeroPoint):
      bestPoint = minusPoint
    elif GoalFunction(zeroPoint) < GoalFunction(plusPoint):
      bestPoint = zeroPoint
    else:
      bestPoint = plusPoint
      
  return bestPoint

def CalculateStepPoint(x, step, coordinate):
  stepPoint = copy(x)
  stepPoint[coordinate] += step
  return stepPoint

def IsXBFartherFromMinThenXN(xb, xn, GoalFunction):
  if GoalFunction(xb) > GoalFunction(xn):
    return True
  return False

def ReflectXBAccrossXN(xb, xn):
  reflectedPoint = []
  for i in range(len(xb)):
    reflectedPoint.append(2*xn[i] - xb[i])
  
  return reflectedPoint

def HalveSteps(steps):
  halvedSteps = []
  for i in range(len(steps)):
    halvedSteps.append(steps[i] / 2.)
  
  return halvedSteps
  
def PrintRow(xb, xp, xn, step):
  row = ""
  row += str(xb)
  row += str(xp)
  row += str(xn)
  row += str(step)
  print row
""""""