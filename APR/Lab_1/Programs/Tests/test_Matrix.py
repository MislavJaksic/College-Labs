from Programs.Matrix import Matrix

import pytest

# @pytest.fixture(scope='module')
# def DatasetFunc():
	# dataset = DatasetLoader.Load(conn, cond)
	# return dataset

# def test_CountValues(DatasetFunc):
	# assert (True == Counter.CountValues(DatasetFunc, dontCount))
  # with pytest.raises(Exception) as e_info:
      # db._IsCollectionPath(notColl)
      
@pytest.fixture(scope='function')
def MatrixDull():
	matrix = Matrix([[1,    22],
                   [333,  4444],
                   [55555,666666]
                  ])
	return matrix
  
@pytest.fixture(scope='function')
def Matrix1234():
	matrix = Matrix([[1, 2],
                   [3, 4],
                  ])
	return matrix

@pytest.fixture(scope='function')
def Matrix2468():
	matrix = Matrix([[2, 4],
                   [6, 8],
                  ])
	return matrix

def test_Matrix__init__Dimensions():
  matrix = Matrix(3,3)
  assert matrix[(3,3)] == 0
  
def test_MatrixDel(MatrixDull):
  del MatrixDull
  with pytest.raises(UnboundLocalError) as e_info:
    print MatrixDull

    
def test_Matrix_CreateZeroesListOfLists(MatrixDull):
  list = [[0,0,0,0],[0,0,0,0]]
  output = MatrixDull._CreateZeroesListOfLists(2, 4)
  assert output == list
  output[0][0] = 5
  assert output[1][0] == 0
  
def test_Matrix_IsListOfLists(MatrixDull):
  list = [[0,0,0,0],[0,0,0,0]]
  output = MatrixDull._IsListOfLists(list)
  assert output == True
  
def test_Matrix_IsListOfListsF(MatrixDull):
  list = [0,0]
  output = MatrixDull._IsListOfLists(list)
  assert output == False
  
def test_Matrix_IsListsSameLength(MatrixDull):
  assert MatrixDull._IsListsSameLength([[2],[2]]) == True

def test_Matrix_IsListsSameLengthF(MatrixDull):
  assert MatrixDull._IsListsSameLength([[2, 2],[2, 2],[2, 2, 2]]) == False
  
def test_Matrix_CountRows(MatrixDull):
  assert MatrixDull._CountRows() == 3
  
def test_Matrix_CountColumns(MatrixDull):
  assert MatrixDull._CountColumns() == 2
  

def test_Matrix_Print(Matrix1234):
  string = '[1, 2]\n[3, 4]\nrows: 2, columns: 2'
  assert str(Matrix1234) == string
  
 
def test_Matrix__getitem__(MatrixDull):
  assert MatrixDull[(2,2)] == 4444
  assert MatrixDull[(1,2)] == 22
  assert MatrixDull[(2,1)] == 333

def test_Matrix_IsKeyInRange(Matrix1234):
  assert Matrix1234._IsKeyInRange((2,2)) == True
  
def test_Matrix_IsKeyInRangeF(Matrix1234):
  assert Matrix1234._IsKeyInRange((2,3)) == False
  assert Matrix1234._IsKeyInRange((0,2)) == False
  assert Matrix1234._IsKeyInRange((1,0)) == False

def test_Matrix__setitem__(MatrixDull):
  MatrixDull[(1,1)] = 0.1
  assert MatrixDull[(1,1)] == 0.1
  
def test_Matrix_IsValidKey(Matrix1234):
  assert Matrix1234._IsValidKey((5,4)) == True

def test_Matrix_IsValidKeyF(Matrix1234):
  assert Matrix1234._IsValidKey([5,4]) == False
  assert Matrix1234._IsValidKey([5]) == False
  assert Matrix1234._IsValidKey(5) == False
  assert Matrix1234._IsValidKey(5/4.) == False
  
  
def test_Matrix__add__(Matrix1234, Matrix2468):
  matrix = Matrix1234 + Matrix2468
  assert Matrix1234[(1,1)] == 1
  assert Matrix2468[(1,1)] == 2
  assert matrix[(1,1)] == 3
  assert matrix[(2,2)] == 12
  
def test_Matrix__sub__(Matrix1234, Matrix2468):
  matrix = Matrix1234 - Matrix2468
  assert matrix[(1,1)] == -1
  assert matrix[(2,2)] == -4
  
def test_Matrix__mul__(Matrix1234, Matrix2468):
  matrix = Matrix1234 * Matrix2468
  assert matrix[(1,1)] == 14
  assert matrix[(2,2)] == 44
  
def test_Matrix__mul__SingleValue():
  matrixManyRows = Matrix([[1], [2], [3], [4], [5]])
  matrixManyColumns = Matrix([[1,2,3,4,5]])
  singleValueMatrix = matrixManyColumns * matrixManyRows
  assert singleValueMatrix[(1,1)] == 55
  
def test_Matrix__mul__Huge():
  matrixManyRows = Matrix([[1], [2], [3], [4], [5]])
  matrixManyColumns = Matrix([[1,2,3,4,5]])
  hugeMatrix = matrixManyRows * matrixManyColumns
  assert hugeMatrix[5,5] == 25

def test_Matrix__mul__E(Matrix1234, MatrixDull):
  with pytest.raises(Exception) as e_info:
    singleValueMatrix = Matrix1234 * MatrixDull
  
def test_Matrix_GetMulDimensions(Matrix1234, MatrixDull):
  assert MatrixDull._GetMulDimensions(Matrix1234) == (3, 2)
  
def test_Matrix_GetMatrixRow(MatrixDull):
  assert MatrixDull._GetMatrixRow(2) == [333, 4444]
  
def test_Matrix_GetMatrixColumn(MatrixDull):
  assert MatrixDull._GetMatrixColumn(2) == [22, 4444, 666666]
  
def test_Matrix_MulRowWithColumn(Matrix1234, MatrixDull):
  row = MatrixDull._GetMatrixRow(1)
  column = Matrix1234._GetMatrixColumn(1)
  assert MatrixDull._MulRowWithColumn(row, column) == 67
  
  
def test_Matrix_transpose(MatrixDull):
  MatrixDull.transpose()
  assert MatrixDull[(1,1)] == 1
  assert MatrixDull[(1,2)] == 333
  assert MatrixDull[(1,3)] == 55555
  assert MatrixDull[(2,1)] == 22
  assert MatrixDull[(2,2)] == 4444
  assert MatrixDull[(2,3)] == 666666
  MatrixDull.transpose()
  assert MatrixDull[(1,1)] == 1
  assert MatrixDull[(1,2)] == 22
  assert MatrixDull[(2,1)] == 333
  assert MatrixDull[(2,2)] == 4444
  assert MatrixDull[(3,1)] == 55555
  assert MatrixDull[(3,2)] == 666666
  
def test_Matrix__eq__(MatrixDull):
  newMatrix = Matrix([[1,    22],
                      [333,  4444],
                      [55555,666666]
                     ])
  assert (MatrixDull == newMatrix) == True
  
def test_Matrix__eq__F(MatrixDull):
  newMatrix = Matrix([[1,    2],
                      [3,4],
                      [5,6]
                     ])
  assert (MatrixDull == newMatrix) == False
  
def test_Matrix_IsMatricesSameDimension(Matrix1234, Matrix2468):
  assert Matrix1234._IsMatricesSameDimension(Matrix2468) == True
  
def test_Matrix_scale(Matrix1234, Matrix2468):
  assert Matrix1234.scale(2) == Matrix2468
 

def test_Matrix__iadd__(Matrix1234, Matrix2468):
  print Matrix1234
  Matrix1234 += Matrix1234
  print Matrix1234
  assert Matrix1234 == Matrix2468
  
def test_Matrix__isub__(Matrix1234, Matrix2468):
  Matrix2468 -= Matrix1234
  assert Matrix1234 == Matrix2468
  

def test_Matrix_toFile_fromFile():
  matrix = Matrix([[1, 2.5],
                   [4, 5.5],
                  ])
  matrix.toFile("output.txt")
  newMatrix = Matrix.fromFile("output.txt")
  assert newMatrix == matrix
  
# def test_Matrix__str__(MatrixDull):
  # print MatrixDull
  # str(MatrixDull)
  
# def test_Matrix__str__(MatrixDull):
  # print MatrixDull
  # str(MatrixDull)
  

  