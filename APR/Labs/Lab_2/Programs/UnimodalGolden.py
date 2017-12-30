import math

golden_ratio = (1 + math.sqrt(5)) / 2 # Golden ratio, 1.6180...

def UnimodalIntervalSearch(startingPoint, step, GoalFunction):
  x0 = startingPoint
  F = GoalFunction
  
  FLeft = F(x0 - step)
  FMiddel = F(x0)
  FRight = F(x0 + step)
  
  if _IsInValley(FLeft, FMiddel, FRight):
    return (x0-step, x0+step)
    
  if not _IsUnimodal(FLeft, FMiddel, FRight):
    raise Exception ("Function is not unimodal; starting point is on a peak.")
  
  inputTrack = []
  inputTrack.append(x0)
  
  outputTrack = []
  outputTrack.append(FMiddel)
  if _IsLeftDescent(FLeft, FMiddel, FRight):
    """      ..
            .
           x0
          .
      ...."""
    inputTrack.append(x0 - step)
    outputTrack.append(FLeft)
    return _FindLeftValley(inputTrack, outputTrack, x0, step, F)
  
  elif _IsRightDescent(FLeft, FMiddel, FRight):
    """..
         .
         x0
           .
            ...."""
    inputTrack.append(x0 + step)
    outputTrack.append(FRight)
    return _FindRightValley(inputTrack, outputTrack, x0, step, F)
    
  elif (FLeft == FMiddel) and (FMiddel == FRight):
    raise Exception ("Function is flat around the starting point: algorithm is directionless.")
    
  else:
    Exception("ERROR_SHOULD_NOT_OCCURE")
 
def _IsLeftDescent(FLeft, FMiddel, FRight):
  if (FLeft < FMiddel) and (FMiddel < FRight):
    return True
  return False
  
def _IsRightDescent(FLeft, FMiddel, FRight):
  if (FLeft > FMiddel) and (FMiddel > FRight):
    return True
  return False
  
  
def _FindLeftValley(inputTrack, outputTrack, x0, step, F):
  i = 1
  while(outputTrack[-1] < outputTrack[-2]):
    x = x0 - step*(2**i)
    
    inputTrack.append(x)
    outputTrack.append(F(x))
    i += 1
    
  return (inputTrack[-1], inputTrack[-3])
  
def _FindRightValley(inputTrack, outputTrack, x0, step, F):
  i = 1
  while(outputTrack[-1] < outputTrack[-2]):
    x = x0 + step*(2**i)
    
    inputTrack.append(x)
    outputTrack.append(F(x))
    i += 1
    
  return (inputTrack[-3], inputTrack[-1])
  
  
def _IsInValley(FLeft, FMiddel, FRight):
  if (FLeft > FMiddel) and (FMiddel < FRight):
    return True
  return False
  
def _IsUnimodal(FLeft, FMiddel, FRight):
  """Asks: is FMiddle a peak?"""
  if (FLeft < FMiddel) and (FMiddel > FRight):
    return False
  return True
  
  
  
def GoldenSectionSearch(startingValue, GoalFunction, epsilon=((0.1)**6), doUnimodal=False):
  """If doUnimodal -> True  -> startingValue is (startingPoint, step)
                   -> False -> startingValue is (A, B)
     A  C  D  B"""
  F = GoalFunction
  
  (A, B) = _GetStartingInterval(startingValue, F, doUnimodal)

  C = B - (B - A) / golden_ratio
  D = A + (B - A) / golden_ratio
  _PrintPoints(A, C, D, B, F) #Deactivate during peformance analysis
  while _IsIntervalBig(A, B, epsilon):
    A, C, D, B = _CalculatePoints(A, C, D, B, F)
    _PrintPoints(A, C, D, B, F) #Deactivate during peformance analysis
      
  return (B + A) / 2
  
def _GetStartingInterval(startingValue, F, doUnimodal):
  if doUnimodal == True:
    (A, B) = UnimodalIntervalSearch(startingValue[0], startingValue[1], F)
  elif doUnimodal == False:
    A = startingValue[0]
    B = startingValue[1]
  else:
    Exception("ERROR_SHOULD_NOT_OCCURE")
  return (A, B)
  
def _IsIntervalBig(A, B, epsilon):
  if abs(B - A) > epsilon:
    return True
  return False
  
def _CalculatePoints(A, C, D, B, F):
  if F(C) < F(D):
    B = D
    D = C
    C = B - (B - A) / golden_ratio 
  else:
    A = C
    C = D
    D = A + (B - A) / golden_ratio
      
  return A, C, D, B
  
def _PrintPoints(A, B, C, D, F):
  print "  A     C     D     B  |  F(A)  F(C)  F(D)  F(B)"
  print "{:+.2f} ".format(A) + "{:+.2f} ".format(C) + "{:+.2f} ".format(D) + "{:+.2f} ".format(B),
  print "{:+.2f} ".format(F(A)) + "{:+.2f} ".format(F(C)) + "{:+.2f} ".format(F(D)) + "{:+.2f} ".format(F(B))
  