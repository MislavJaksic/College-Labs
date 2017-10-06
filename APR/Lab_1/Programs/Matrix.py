# https://docs.python.org/2.7/reference/datamodel.html#emulating-container-types

from InputController import InputController

from copy import copy, deepcopy
from types import TupleType, IntType

class Matrix(object):
  """'Private' methods are prefixed with an underscore (_).
     'Public' methods have a lowercase first letter.
     __method__ are Python data models (or "magic methods") that overrride or add Python functionalities.
     CamelCase.
     Designed to support problem domain abstractions. Indexed from 1 to n/m.
     Exceptions are raised as soon as possible, but outside _Is boolean functions. This is because returning
       a large number of error codes would complicate code more then dealing with exceptions at runtime.
     i1,j1  i1,j2  i1,j3
     i2,j1  i2,j2  i2,j3
     i3,j1  i3,j2  i3,j3
     """
     
  def __init__(self, *input):
    if self._IsGivenMatrixDimensions(input):
      rows, columns = self._ExtractDimensions(input)
      listOfLists = self._CreateZeroesListOfLists(rows, columns)
      
    elif self._IsGivenListOfLists(self._UnwrapTuple(input)):
      listOfLists = self._UnwrapTuple(input)
      
    else:
      raise Exception(u"Create Matrix with dimensions    -> Matrix(rows, columns) or \n"
                      u"Create Matrix with list of lists -> Matrix([ [_num, _num], [_num, _num] ])")
    
    self._SetMatrixAndDimensions(listOfLists)
       
    """Python data models: every object has: an identity: never changes; compared with 'is'; id() returns an integer representing identity
                                             a type: never changes; determines the operations the object supports and values the object can have; type() returns type
                                             a value: may change (mutable) or it may not (immutable);
                                             """
  
  def _IsGivenMatrixDimensions(self, dimensions):
    if self._IsValidKeyValues(dimensions):
      return True
    return False
  
  def _ExtractDimensions(self, tuple):
    return tuple[0], tuple[1]
  
  def _CreateZeroesListOfLists(self, rows, columns):
    zeroesListOfLists = []
    zeroesList = []
    for count in range(columns):
      zeroesList.append(0)
    for count in range(rows):
      zeroesListOfLists.append(copy(zeroesList))
    
    return zeroesListOfLists
    
  def _IsGivenListOfLists(self, matrix):
    if not self._IsListOfLists(matrix):
      return False
    if not self._IsListsSameLength(matrix):
      return False
    return True
    
  def _IsListOfLists(self, matrix):
    if InputController.IsList(matrix):
      for row in matrix:
        if not InputController.IsList(row):
          return False
    else:
      return False
    
    return True
    
  def _IsListsSameLength(self, matrix):
    length = len(matrix[0])
    for row in matrix:
      if not (length == len(row)):
        return False
    return True
  
  def _UnwrapTuple(self, tuple):
    return tuple[0]
  
  
  def _CountRows(self):
    return len(self._matrix)
    
  def _CountColumns(self):
    return len(self._matrix[0])
  
  
  def __str__(self):
    """print A or str(A)
       """
    pretty_matrix = ""
    for row in self._matrix:
      pretty_matrix += str(row)
      pretty_matrix += "\n"
    pretty_matrix += "rows: " + str(self.n_rows) + ", "
    pretty_matrix += "columns: " + str(self.m_columns)
    return pretty_matrix
  
  
  def __getitem__(self, key):
    """A[(row, column)] returns an element
       """
    if not self._IsValidKey(key):
      raise TypeError
    if not self._IsKeyInRange(key):
      raise IndexError
      
    i, j = self._GetZeroIndexes(key)
    
    element = self._matrix[i][j]
    return element
    
  def _IsKeyInRange(self, key):
    rows = key[0]
    columns = key[1]
    if (1 <= rows) and (rows <= self.n_rows):
      if (1 <= columns) and (columns <= self.m_columns):
        return True
      else:
        return False
    else:
      return False
  
  def __setitem__(self, key, value):
    """A[(row, column)] = value
       """
    if not self._IsValidKey(key):
      raise TypeError
    if not self._IsValueNumeric(value):
      raise TypeError 
      
    i, j = self._GetZeroIndexes(key)
    self._matrix[i][j] = value
    
  def _IsValidKey(self, key):
    """Valid key -> (row, columns) where row and columns are integers
       """
    if InputController.IsTuple(key):
      if not self._IsValidKeyValues(key):
        return False
    else:
      return False
    
    return True
  
  def _IsValueNumeric(self, value):
    if InputController.IsInt(value):
      return True
    if InputController.IsFloat(value):
      return True
      
    return False
  
  def _GetZeroIndexes(self, key):
    """(rows, columns)  -> (i, j)
       (1 to n, 1 to m) -> (0 to n-1, 0 to m-1)
       """
    i = key[0] - 1
    j = key[1] - 1
    return i, j
    
  def _IsValidKeyValues(self, key):
    """There has to be only two integer values in a tuple
       """
    countValues = 0
    for value in key:
      if not InputController.IsInt(value):
        return False
      countValues += 1
      
    if (countValues != 2):
      return False
      
    return True
  
  
  def __add__(self, other):
    # if not self._IsSameDimension(other): TODO
      # raise Exception(u"Matrices are not of the same dimnsion.")
    zeroesMatrix = Matrix(self.n_rows, self.m_columns)
    
    for row in range(1, self.n_rows+1):
      for column in range(1, self.m_columns+1):
        zeroesMatrix[(row, column)] = self[(row, column)] + other[(row, column)]
    return zeroesMatrix
    
  def __sub__(self, other):
    # if not self._IsSameDimension(other): TODO
      # raise Exception(u"Matrices are not of the same dimnsion.")
    zeroesMatrix = Matrix(self.n_rows, self.m_columns)
    
    for row in range(1, self.n_rows+1):
      for column in range(1, self.m_columns+1):
        zeroesMatrix[(row, column)] = self[(row, column)] - other[(row, column)]
    return zeroesMatrix
    
  def __mul__(self, other):
    """       |
       ---> * |
              V
       """
    mulRows, mulColumns = self._GetMulDimensions(other)
    zeroesMatrix = Matrix(mulRows, mulColumns)
    
    for row in range(1, mulRows+1):
      for column in range(1, mulColumns+1):
        result = self._MulRowWithColumn(self._GetMatrixRow(row), other._GetMatrixColumn(column))
        zeroesMatrix[(row, column)] = result
    return zeroesMatrix
    
  def _GetMulDimensions(self, other):
    if not self._IsMulDimension(other):
      raise Exception(u"Matrices are not of the dimnsions that they can be multiplied.")
    return self.n_rows, other.m_columns
    
  def _IsMulDimension(self, other):
    if (self.m_columns == other.n_rows):
      return True
    return False
    
  def _GetMatrixRow(self, row):
    i = row - 1
    return self._matrix[i]
    
  def _GetMatrixColumn(self, column):
    matrixColumn = []
    for row in range(1, self.n_rows+1):
      matrixColumn.append(self[(row, column)])
    return matrixColumn
    
  def _MulRowWithColumn(self, rowList, columnList):
    sum = 0
    for index in range(len(rowList)):
      sum += rowList[index] * columnList[index]
    return sum
  
  
  def transpose(self):
    """A(ij) -> swap row and column value (and indexes) -> A(ji)
       Graphical solution: find the main diagonal and swap elements across it.
                   t   [1 5]
       [1 2 3 4]  -->  [2 6]
       [5 6 7 8]       [3 7]
                       [4 8]
       """
    tRows = self.m_columns
    tColumns = self.n_rows
    zeroesListOfLists = self._CreateZeroesListOfLists(tRows, tColumns)
    
    for row in range(1, self.n_rows+1):
      for column in range(1, self.m_columns+1):
        zeroesListOfLists[column-1][row-1] = self[(row, column)]
    self._SetMatrixAndDimensions(zeroesListOfLists)
    return self
  
  def _SetMatrixAndDimensions(self, listOfLists):
    self._matrix = listOfLists 
    self.n_rows = self._CountRows()
    self.m_columns = self._CountColumns()
   
  def __eq__(self, other):
    if not self._IsMatricesSameDimension(other):
      return False
    for row in range(1, self.n_rows+1):
      for column in range(1, self.m_columns+1):
        if not self._IsFloatsEqual(self[(row, column)], other[(row, column)]):
          return False
    return True
    
  def _IsFloatsEqual(self, floatOne, floatTwo):
    """If f1 close to f2 then expand f2 by adding and subtracting a margin of error
       """
    error = (0.1)**6
    if ((floatTwo-error) < floatOne) and (floatOne < (floatTwo+error)):
      return True
    return False
    
  def _IsMatricesSameDimension(self, other):
    if not (self.n_rows == other.n_rows):
      return False
    if not (self.m_columns == other.m_columns):
      return False
    return True
    
  def scale(self, scalar_value):
    for row in range(1, self.n_rows+1):
      for column in range(1, self.m_columns+1):
        self[(row, column)] = scalar_value * self[(row, column)]
    return self
  
  # def _GetNext_i_j(self):
    
    # yield i, j
    
  # def _GetNext_row_column(self):
    
    # yield row, column
    
  def __iadd__(self, other):
    """A += B"""
    self = self + other
    return self
  
  def __isub__(self, other):
    """A -= B"""
    self = self - other
    return self
  
  @staticmethod
  def fromFile(path):
    listOfLists = []
    with open(path, "r") as f:
      for line in f:
        stringList = line.split(" ")
        
        list = []
        for string in stringList:
          number = _ConvertToNumber(string)
          list.append(number)
          
        listOfLists.append(list)
        
    return Matrix(listOfLists)
    
  def toFile(self, path):
    with open(path, "w") as f:
      for row in self._matrix:
        stringRow = []
        for number in row:
          stringRow.append(str(number))
        line = " ".join(stringRow)
        f.write(line)
        f.write("\n")
        
  
  def LU(self):
    for pivotCoord in range(1, self.n_rows):
      self._DivideBelow(pivotCoord)
      self._SubBelowAndRightOf(pivotCoord)
    
    L, U = self._CreateLU()
    return L, U
    
  def LUP(self):
    P = self._CreateP()
    for pivotCoord in range(1, self.n_rows):
      l = self._FindRowWithLargestValueInColumn(pivotCoord)
      
      self._SwapRows(pivotCoord, l)
      
      P._SwapRows(pivotCoord, l)
        
      self._DivideBelow(pivotCoord)
      self._SubBelowAndRightOf(pivotCoord)
      
    L, U = self._CreateLU()
    return L, U, P
  
  def _DivideBelow(self, k):
    for i in range(k+1, self.n_rows+1):
      if self._IsFloatsEqual(self[(k, k)], 0.0):
        raise ZeroDivisionError
      self[(i, k)] = self[(i, k)] / float(self[(k, k)])
  
  def _SubBelowAndRightOf(self, k):
    for i in range(k+1, self.n_rows+1):
      for j in range(k+1, self.n_rows+1):
        self[(i, j)] = self[(i, j)] - self[(i, k)] * self[(k, j)]
  
  def _FindRowWithLargestValueInColumn(self, k):
    pivot = 0.0
    for i in range(k, self.n_rows+1):
      if (abs(self[(i, k)]) > pivot):
        pivot = abs(self[(i, k)])
        l = i
    if self._IsFloatsEqual(pivot, 0.0):
      raise ZeroDivisionError
    return l
  
  def _SwapRows(self, rowOne, rowTwo):
    i = rowOne - 1
    j = rowTwo - 1
    guardian = deepcopy(self._matrix[i])
    self._matrix[i] = deepcopy(self._matrix[j])
    self._matrix[j] = guardian
  
  def _CreateP(self):
    P = Matrix(self.n_rows, self.n_rows)
    for i in range(1, self.n_rows+1):
      P[(i, i)] = 1
    return P
  
  def _CreateLU(self):
    L = Matrix(self.n_rows, self.n_rows)
    U = Matrix(self.n_rows, self.n_rows)
    for row in range(1, self.n_rows+1):
      for column in range(1, self.n_rows+1):
        if (column >= row):
          U[(row, column)] = self[row, column]
        else:
          L[(row, column)] = self[row, column]
        if (column == row):
          L[(row, column)] = 1
    return L, U

    
  def _solveLyPb(self, L, P, b):
    """Inplace Foward Substitution, L*y=P*b"""
    b = P * b
    y = deepcopy(b)
    for i in range(1, self.n_rows):
      for j in range(i+1, self.n_rows+1):
        y[(j, 1)] -= L[(j, i)] * y[(i, 1)]
    return y
  
  def _solveUxy(self, U, y):
    """Inplace Backward Substitution, U*x=y"""
    x = deepcopy(y)
    for i in range(self.n_rows, 0, -1):
      x[(i, 1)] /= float(U[(i, i)])
      for j in range(1, i):
        x[(j, 1)] -= U[(j, i)] * x[(i, 1)]
    return x
        
  def solveAxbWithLU(self, A, b):
    L, U = A.LU()
    P = self._CreateP()
    y = self._solveLyPb(L, P, b)
    x = self._solveUxy(U, y)
    return x, y
    
  def solveAxbWithLUP(self, A, b):
    L, U, P = A.LUP()
    y = self._solveLyPb(L, P, b)
    x = self._solveUxy(U, y)
    return x, y
    
    
def _ConvertToNumber(string):
    if (string.find(".") != -1):
      return float(string)
    else:
      return int(string)
    