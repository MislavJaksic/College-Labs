import Programs.UnimodalGolden

import pytest
  
def PeakFunction(x):
  return (-1)*x*x + 3
  
def ValleyFunction(x):
  return x*x + 3
  
def Helper(startingPoint, step, GoalFunction):
  x0 = startingPoint
  F = GoalFunction
  
  FLeft = F(x0 - step)
  FMiddel = F(x0)
  FRight = F(x0 + step)
  
  return x0, F, FLeft, FMiddel, FRight

def test_UnimodalGolden_IsUnimodalT():
  x0, F, FLeft, FMiddel, FRight = Helper(0, 1, ValleyFunction)
  assert Programs.UnimodalGolden._IsUnimodal(FLeft, FMiddel, FRight) == True
  
def test_UnimodalGolden_IsUnimodalF():
  x0, F, FLeft, FMiddel, FRight = Helper(0, 1, PeakFunction)
  assert Programs.UnimodalGolden._IsUnimodal(FLeft, FMiddel, FRight) == False

    
def test_UnimodalGolden_IsInValleyT():
  x0, F, FLeft, FMiddel, FRight = Helper(0, 1, ValleyFunction)
  assert Programs.UnimodalGolden._IsInValley(FLeft, FMiddel, FRight) == True
  
def test_UnimodalGolden_IsInValleyF():
  x0, F, FLeft, FMiddel, FRight = Helper(0, 1, PeakFunction)
  assert Programs.UnimodalGolden._IsInValley(FLeft, FMiddel, FRight) == False
  
  
def test_UnimodalGolden_IsLeftDescentT():
  x0, F, FLeft, FMiddel, FRight = Helper(5, 1, ValleyFunction)
  assert Programs.UnimodalGolden._IsLeftDescent(FLeft, FMiddel, FRight) == True
  
def test_UnimodalGolden_IsLeftDescentF():
  x0, F, FLeft, FMiddel, FRight = Helper(-5, 1, ValleyFunction)
  assert Programs.UnimodalGolden._IsLeftDescent(FLeft, FMiddel, FRight) == False

    
def test_UnimodalGolden_IsRightDescentT():
  x0, F, FLeft, FMiddel, FRight = Helper(-5, 1, ValleyFunction)
  assert Programs.UnimodalGolden._IsRightDescent(FLeft, FMiddel, FRight) == True
  
def test_UnimodalGolden_IsRightDescentF():
  x0, F, FLeft, FMiddel, FRight = Helper(5, 1, ValleyFunction)
  assert Programs.UnimodalGolden._IsRightDescent(FLeft, FMiddel, FRight) == False
  
  
def test_UnimodalGolden_FindLeftValley():
  x0, F, FLeft, FMiddel, FRight = Helper(5, 1, ValleyFunction)
  step = 1
  inputTrack = []
  inputTrack.append(x0)
  inputTrack.append(x0 - step)
  outputTrack = []
  outputTrack.append(FMiddel)
  outputTrack.append(FLeft)
  assert Programs.UnimodalGolden._FindLeftValley(inputTrack, outputTrack, x0, step, F) == (-3, 3)
  
def test_UnimodalGolden_FindRightValley():
  x0, F, FLeft, FMiddel, FRight = Helper(-5, 1, ValleyFunction)
  step = 1
  inputTrack = []
  inputTrack.append(x0)
  inputTrack.append(x0 + step)
  outputTrack = []
  outputTrack.append(FMiddel)
  outputTrack.append(FRight)
  assert Programs.UnimodalGolden._FindRightValley(inputTrack, outputTrack, x0, step, F) == (-3, 3)

def test_UnimodalGoldenUnimodalIntervalSearchE1():
  startingPoint = 100
  step = 1
  GoalFunction = lambda x: (x*x -2)
  assert Programs.UnimodalGolden.UnimodalIntervalSearch(startingPoint, step, GoalFunction) == (-156, 36)
  
def test_UnimodalGoldenUnimodalIntervalSearchE2():
  startingPoint = 0
  step = 1
  GoalFunction = lambda x: (x - 4)**2
  assert Programs.UnimodalGolden.UnimodalIntervalSearch(startingPoint, step, GoalFunction) == (2, 8)
  
def test_UnimodalGoldenUnimodalIntervalSearchDirectionless():
  startingPoint = 0
  step = 1
  GoalFunction = lambda x: 1
  with pytest.raises(Exception) as e_info:
    Programs.UnimodalGolden.UnimodalIntervalSearch(startingPoint, step, GoalFunction)
    
    
def test_UnimodalGolden_GetStartingIntervalT():
  startingPoint = 100
  step = 1
  GoalFunction = lambda x: (x*x -2)
  assert Programs.UnimodalGolden._GetStartingInterval((100, 1), GoalFunction, doUnimodal=True) == (-156, 36)

def test_UnimodalGolden_GetStartingIntervalF():
  GoalFunction = lambda x: (x*x -2)
  assert Programs.UnimodalGolden._GetStartingInterval((-156, 36), GoalFunction, doUnimodal=False) == (-156, 36)
   
def test_UnimodalGoldenGoldenSectionSearch():
  GoalFunction = lambda x: (x - 4)**2
  result = Programs.UnimodalGolden.GoldenSectionSearch((2, 8), GoalFunction, doUnimodal=False)
  assert (3.9 < result < 4.1) == True
    