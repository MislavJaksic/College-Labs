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

def test_Matrix__init__EmptyWithDimensions():
  matrix = Matrix(3,3)
  assert matrix[(3,3)] == 0
  
def test_MatrixDel(MatrixDull):
  del MatrixDull
  with pytest.raises(UnboundLocalError) as e_info:
    print MatrixDull
 
def test_Matrix__getitem__(MatrixDull):
  assert MatrixDull[(2,2)] == 4444
  
def test_Matrix__getitem__Small():
  matrix = Matrix([[1,2],
                  ])
  assert matrix[(1,2)] == 2

def test_Matrix_IsListsSameLength(MatrixDull):
  assert MatrixDull._IsListsSameLength([[2],[2]]) == True

def test_Matrix_IsListsSameLengthF(MatrixDull):
  assert MatrixDull._IsListsSameLength([[2, 2],[2, 2],[2, 2, 2]]) == False
  
def test_Matrix_CountRows(MatrixDull):
  assert MatrixDull._CountRows() == 3
  
def test_Matrix_CountColumns(MatrixDull):
  assert MatrixDull._CountColumns() == 2
  
def test_Matrix__str__(MatrixDull):
  print MatrixDull
  str(MatrixDull)
  
def test_Matrix__setitem__(MatrixDull):
  MatrixDull[(1,1)] = 0.1
  assert MatrixDull[(1,1)] == 0.1
  
def test_Matrix_IsValidKeyT(MatrixDull):
  assert MatrixDull._IsValidKey((122, -14)) == True
  
def test_Matrix_IsValidKeyFList(MatrixDull):
  assert MatrixDull._IsValidKey([122, -14]) == False
  
def test_Matrix_IsValidKeyFOneValue(MatrixDull):
  assert MatrixDull._IsValidKey((122)) == False
  
def test_Matrix_IsValidKeyFTooManyValues(MatrixDull):
  assert MatrixDull._IsValidKey((122, 1, 2)) == False

def test_Matrix_IsKeyInRange(MatrixDull):
  assert MatrixDull._IsKeyInRange((1, 2)) == True
  
def test_Matrix_IsKeyInRangeF(MatrixDull):
  assert MatrixDull._IsKeyInRange((3, 3)) == False
  
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
  
# def test_Matrix__str__(MatrixDull):
  # print MatrixDull
  # str(MatrixDull)
  
# def test_Matrix__str__(MatrixDull):
  # print MatrixDull
  # str(MatrixDull)
  

  