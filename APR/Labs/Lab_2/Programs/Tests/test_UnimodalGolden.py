import Programs.UnimodalGolden

import pytest

# @pytest.fixture(scope='module')
# def DatasetFunc():
	# dataset = DatasetLoader.Load(conn, cond)
	# return dataset

# def test_CountValues(DatasetFunc):
	# assert (True == Counter.CountValues(DatasetFunc, dontCount))
  # with pytest.raises(Exception) as e_info:
      # db._IsCollectionPath(notColl)
      
# @pytest.fixture(scope='function')
# def MatrixDull():
	# matrix = Matrix([[1,    22],
                   # [333,  4444],
                   # [55555,666666]
                  # ])
	# return matrix
  
# @pytest.fixture(scope='function')
# def Matrix1234():
	# matrix = Matrix([[1, 2],
                   # [3, 4],
                  # ])
	# return matrix
  
# @pytest.fixture(scope='function')
# def Matrix2468():
	# matrix = Matrix([[2, 4],
                   # [6, 8],
                  # ])
	# return matrix

# @pytest.fixture(scope='function')
# def Matrix120():
  # matrix = Matrix([[1, 2, 0],
                   # [3, 5, 4],
                   # [5, 6, 3],
                  # ])
  # return matrix
  
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
    
""""""
# def test_UnimodalGolden_IsListOfListsF(UnimodalGoldenDull):
  # list = [0,0]
  # output = UnimodalGoldenDull._IsListOfLists(list)
  # assert output == False
  
# def test_UnimodalGolden_IsListsSameLength(UnimodalGoldenDull):
  # assert UnimodalGoldenDull._IsListsSameLength([[2],[2]]) == True

# def test_UnimodalGolden_IsListsSameLengthF(UnimodalGoldenDull):
  # assert UnimodalGoldenDull._IsListsSameLength([[2, 2],[2, 2],[2, 2, 2]]) == False
  
# def test_UnimodalGolden_CountRows(UnimodalGoldenDull):
  # assert UnimodalGoldenDull._CountRows() == 3
  
# def test_UnimodalGolden_CountColumns(UnimodalGoldenDull):
  # assert UnimodalGoldenDull._CountColumns() == 2
  

# def test_UnimodalGolden_Print(UnimodalGolden1234):
  # string = '[1, 2]\n[3, 4]\n'
  # assert str(UnimodalGolden1234) == string
  
 
# def test_UnimodalGolden__getitem__(UnimodalGoldenDull):
  # assert UnimodalGoldenDull[(2,2)] == 4444
  # assert UnimodalGoldenDull[(1,2)] == 22
  # assert UnimodalGoldenDull[(2,1)] == 333

# def test_UnimodalGolden_IsKeyInRange(UnimodalGolden1234):
  # assert UnimodalGolden1234._IsKeyInRange((2,2)) == True
  
# def test_UnimodalGolden_IsKeyInRangeF(UnimodalGolden1234):
  # assert UnimodalGolden1234._IsKeyInRange((2,3)) == False
  # assert UnimodalGolden1234._IsKeyInRange((0,2)) == False
  # assert UnimodalGolden1234._IsKeyInRange((1,0)) == False

# def test_UnimodalGolden__setitem__(UnimodalGoldenDull):
  # UnimodalGoldenDull[(1,1)] = 0.1
  # assert UnimodalGoldenDull[(1,1)] == 0.1
  
# def test_UnimodalGolden_IsValidKey(UnimodalGolden1234):
  # assert UnimodalGolden1234._IsValidKey((5,4)) == True

# def test_UnimodalGolden_IsValidKeyF(UnimodalGolden1234):
  # assert UnimodalGolden1234._IsValidKey([5,4]) == False
  # assert UnimodalGolden1234._IsValidKey([5]) == False
  # assert UnimodalGolden1234._IsValidKey(5) == False
  # assert UnimodalGolden1234._IsValidKey(5/4.) == False
  
  
# def test_UnimodalGolden__add__(UnimodalGolden1234, UnimodalGolden2468):
  # matrix = UnimodalGolden1234 + UnimodalGolden2468
  # assert UnimodalGolden1234[(1,1)] == 1
  # assert UnimodalGolden2468[(1,1)] == 2
  # assert matrix[(1,1)] == 3
  # assert matrix[(2,2)] == 12
  
# def test_UnimodalGolden__sub__(UnimodalGolden1234, UnimodalGolden2468):
  # matrix = UnimodalGolden1234 - UnimodalGolden2468
  # assert matrix[(1,1)] == -1
  # assert matrix[(2,2)] == -4
  
# def test_UnimodalGolden__mul__(UnimodalGolden1234, UnimodalGolden2468):
  # matrix = UnimodalGolden1234 * UnimodalGolden2468
  # assert matrix[(1,1)] == 14
  # assert matrix[(2,2)] == 44
  
# def test_UnimodalGolden__mul__SingleValue():
  # matrixManyRows = UnimodalGolden([[1], [2], [3], [4], [5]])
  # matrixManyColumns = UnimodalGolden([[1,2,3,4,5]])
  # singleValueUnimodalGolden = matrixManyColumns * matrixManyRows
  # assert singleValueUnimodalGolden[(1,1)] == 55
  
# def test_UnimodalGolden__mul__Huge():
  # matrixManyRows = UnimodalGolden([[1], [2], [3], [4], [5]])
  # matrixManyColumns = UnimodalGolden([[1,2,3,4,5]])
  # hugeUnimodalGolden = matrixManyRows * matrixManyColumns
  # assert hugeUnimodalGolden[5,5] == 25

# def test_UnimodalGolden__mul__E(UnimodalGolden1234, UnimodalGoldenDull):
  # with pytest.raises(Exception) as e_info:
    # singleValueUnimodalGolden = UnimodalGolden1234 * UnimodalGoldenDull
  
# def test_UnimodalGolden_GetMulDimensions(UnimodalGolden1234, UnimodalGoldenDull):
  # assert UnimodalGoldenDull._GetMulDimensions(UnimodalGolden1234) == (3, 2)
  
# def test_UnimodalGolden_GetUnimodalGoldenRow(UnimodalGoldenDull):
  # assert UnimodalGoldenDull._GetUnimodalGoldenRow(2) == [333, 4444]
  
# def test_UnimodalGolden_GetUnimodalGoldenColumn(UnimodalGoldenDull):
  # assert UnimodalGoldenDull._GetUnimodalGoldenColumn(2) == [22, 4444, 666666]
  
# def test_UnimodalGolden_MulRowWithColumn(UnimodalGolden1234, UnimodalGoldenDull):
  # row = UnimodalGoldenDull._GetUnimodalGoldenRow(1)
  # column = UnimodalGolden1234._GetUnimodalGoldenColumn(1)
  # assert UnimodalGoldenDull._MulRowWithColumn(row, column) == 67
  
  
# def test_UnimodalGolden_transpose(UnimodalGoldenDull):
  # UnimodalGoldenDull.transpose()
  # assert UnimodalGoldenDull[(1,1)] == 1
  # assert UnimodalGoldenDull[(1,2)] == 333
  # assert UnimodalGoldenDull[(1,3)] == 55555
  # assert UnimodalGoldenDull[(2,1)] == 22
  # assert UnimodalGoldenDull[(2,2)] == 4444
  # assert UnimodalGoldenDull[(2,3)] == 666666
  # UnimodalGoldenDull.transpose()
  # assert UnimodalGoldenDull[(1,1)] == 1
  # assert UnimodalGoldenDull[(1,2)] == 22
  # assert UnimodalGoldenDull[(2,1)] == 333
  # assert UnimodalGoldenDull[(2,2)] == 4444
  # assert UnimodalGoldenDull[(3,1)] == 55555
  # assert UnimodalGoldenDull[(3,2)] == 666666
  
# def test_UnimodalGolden__eq__(UnimodalGoldenDull):
  # newUnimodalGolden = UnimodalGolden([[1,    22],
                      # [333,  4444],
                      # [55555,666666]
                     # ])
  # assert (UnimodalGoldenDull == newUnimodalGolden) == True
  
# def test_UnimodalGolden__eq__F(UnimodalGoldenDull):
  # newUnimodalGolden = UnimodalGolden([[1,    2],
                      # [3,4],
                      # [5,6]
                     # ])
  # assert (UnimodalGoldenDull == newUnimodalGolden) == False
  
# def test_UnimodalGolden_IsMatricesSameDimension(UnimodalGolden1234, UnimodalGolden2468):
  # assert UnimodalGolden1234._IsMatricesSameDimension(UnimodalGolden2468) == True
  
# def test_UnimodalGolden_scale(UnimodalGolden1234, UnimodalGolden2468):
  # assert UnimodalGolden1234.scale(2) == UnimodalGolden2468
 

# def test_UnimodalGolden__iadd__(UnimodalGolden1234, UnimodalGolden2468):
  # print UnimodalGolden1234
  # UnimodalGolden1234 += UnimodalGolden1234
  # print UnimodalGolden1234
  # assert UnimodalGolden1234 == UnimodalGolden2468
  
# def test_UnimodalGolden__isub__(UnimodalGolden1234, UnimodalGolden2468):
  # UnimodalGolden2468 -= UnimodalGolden1234
  # assert UnimodalGolden1234 == UnimodalGolden2468
  

# def test_UnimodalGolden_toFile_fromFile():
  # matrix = UnimodalGolden([[1, 2.5],
                   # [4, 5.5],
                  # ])
  # matrix.toFile("output.txt")
  # newUnimodalGolden = UnimodalGolden.fromFile("output.txt")
  # assert newUnimodalGolden == matrix
  
  
# def test_UnimodalGolden_LU():
  # list = [[2,3,1,5],
          # [6,13,5,19],
          # [2,19,10,23],
          # [4,10,11,31],
         # ]
  # LU = [[2,3,1,5],
        # [3,4,2,4],
        # [1,4,1,2],
        # [2,1,7,3],
       # ]
  # LTrue = [[1,0,0,0],
       # [3,1,0,0],
       # [1,4,1,0],
       # [2,1,7,1],
      # ]
  # UTrue = [[2,3,1,5],
       # [0,4,2,4],
       # [0,0,1,2],
       # [0,0,0,3],
      # ]
  # matrix = UnimodalGolden(list)
  # L, U = UnimodalGolden.LU(matrix)
  # assert matrix == UnimodalGolden(list)
  
  # assert matrix == UnimodalGolden(LU)
  # assert L == UnimodalGolden(LTrue)
  # assert U == UnimodalGolden(UTrue)
  
# def test_UnimodalGolden_LUP(UnimodalGolden120):
  # list = [[1, 2, 0],
          # [3, 5, 4],
          # [5, 6, 3],
         # ]
  # LUP = [[5, 6, 3],
        # [3/5., 7/5., 11/5.],
        # [1/5., 4/7., -13/7.],
        # ]
  # LTrue = [[1, 0, 0],
       # [3/5., 1, 0],
       # [1/5., 4/7., 1],
      # ]
  # UTrue = [[5, 6, 3],
       # [0, 7/5., 11/5.],
       # [0, 0, -13/7.],
      # ]
  # PTrue = [[0, 0, 1],
       # [0, 1, 0],
       # [1, 0, 0],
      # ]
  # L, U, P = UnimodalGolden.LUP(UnimodalGolden120)
  # assert UnimodalGolden120 == UnimodalGolden(list)
  # assert UnimodalGolden120 == UnimodalGolden(LUP)
  # assert L == UnimodalGolden(LTrue)
  # assert U == UnimodalGolden(UTrue)
  # assert P == UnimodalGolden(PTrue)
  
  
# def test_UnimodalGolden_solveLyPb(UnimodalGolden120):
  # b = UnimodalGolden([[0.1],
              # [12.5],
              # [10.3]])
  # L, U = UnimodalGolden.LU(UnimodalGolden120)
  # P = UnimodalGolden120._CreateI()
  # y = UnimodalGolden120._solveLyPb(L, P, b)
  # assert y == UnimodalGolden([[0.1], [12.2], [-39]])
  # x = UnimodalGolden120._solveUxy(U, y)
  # assert x == UnimodalGolden([[0.5], [-0.2], [3]])
  
# def test_UnimodalGolden_solveUxy(UnimodalGolden120):
  # b = UnimodalGolden([[0.1],
              # [12.5],
              # [10.3]])
  # L, U, P = UnimodalGolden.LUP(UnimodalGolden120)
  # y = UnimodalGolden120._solveLyPb(L, P, b)
  # assert y == UnimodalGolden([[10.3], [6.319999], [-5.571428]])
  # x = UnimodalGolden120._solveUxy(U, y)
  # assert x == UnimodalGolden([[0.5], [-0.2], [3]])
  
# def test_UnimodalGolden_solveAxbWithLU(UnimodalGolden120):
  # b = UnimodalGolden([[0.1],
              # [12.5],
              # [10.3]])
  # x, y = UnimodalGolden.solveAxbWithLU(UnimodalGolden120, b)
  # assert y == UnimodalGolden([[0.1], [12.2], [-39]])
  # assert x == UnimodalGolden([[0.5], [-0.2], [3]])
  
# def test_UnimodalGolden_solveAxbWithLUP(UnimodalGolden120):
  # b = UnimodalGolden([[0.1],
              # [12.5],
              # [10.3]])
  # x, y = UnimodalGolden.solveAxbWithLUP(UnimodalGolden120, b)
  # assert y == UnimodalGolden([[10.3], [6.319999], [-5.571428]])
  # assert x == UnimodalGolden([[0.5], [-0.2], [3]])
  
# def test_UnimodalGolden_inverse():
  # A = UnimodalGolden([[1, 2],
              # [3, 4],
             # ])
  # result = UnimodalGolden([[-2, 1],
                   # [3/2., -1/2.],
                  # ])
  # A.inverse()
  # assert A == result