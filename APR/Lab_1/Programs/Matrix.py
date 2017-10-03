# https://docs.python.org/2.7/reference/datamodel.html#emulating-container-types

from InputController import InputController

from copy import copy, deepcopy
from types import TupleType, IntType

class Matrix(object):
  """'Private' methods are prefixed with an underscore (_).
     'Public' methods have a lowercase first letter.
     __method__ are data objects (or "magic methods") that overrride or add Python functionalities.
     CamelCase.
     Designed to support problem domain abstractions. Indexed from 1 to n/m.
     i1,j1  i1,j2  i1,j3
     i2,j1  i2,j2  i2,j3
     i3,j1  i3,j2  i3,j3
     """
     
  def __init__(self, *values):
    """*values is a tuple.
       If given dimensions i_rows, j_columns -> Construct an zeroes matrix.
       If given a single list in a list      -> Construct a matrix with a single row.
       If given many lists in a list         -> Construct a matrix made up of many rows."""
    if self._IsGivenMatrixDimensions(values):
      rows = values[0]
      columns = values[1]
      matrix = self._CreateZeroesMatrix(rows, columns)
      
    elif self._IsGivenListOfLists(self._UnwrapTuple(values)):
      matrix = deepcopy(self._UnwrapTuple(values))
      
    else:
      raise Exception(u"Create Matrix with dimensions rows, columns -> Matrix(rows, columns) or \n"
                      u"Create Matrix with list of lists            -> Matrix([ [_num, _num], [_num, _num] ])")
    
    self._matrix = matrix 
    self.n_rows = self._CountRows()
    self.m_columns = self._CountColumns()
       
    """Python data models: every object has: an identity: never changes; compared with 'is'; id() returns an integer representing identity
                                             a type: never changes; determines the operations the object supports and values the object can have; type() returns type
                                             a value: may change (mutable) or it may not (immutable);
                                             """
                                             
  def _CreateZeroesMatrix(self, rows, columns):
    zeroesListOfLists = []
    zeroesList = []
    for count in range(columns):
      zeroesList.append(0)
    for count in range(rows):
      zeroesListOfLists.append(copy(zeroesList))
    
    return zeroesListOfLists
    
  def _IsGivenMatrixDimensions(self, dimensions):
    if self._IsValidKeyValues(dimensions):
      return True
    return False
    
  def _IsGivenListOfLists(self, matrix):
    if not self._IsListOfLists(matrix):
      raise Exception(u"Given something other then a list")
    if not self._IsListsSameLength(matrix):
      raise Exception(u"Unequal number of elements in lists")
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
    pretty_matrix = ""
    for row in self._matrix:
      pretty_matrix += str(row)
      pretty_matrix += "\n"
    pretty_matrix += "i_rows: " + str(self.n_rows) + ", "
    pretty_matrix += "j_columns: " + str(self.m_columns)
    return pretty_matrix
  
  def __getitem__(self, key):
    """Called to implement evaluation of matrix[key].
       A[(i, j)] returns element in row i and column j."""
    if not self._IsValidKey(key):
      raise TypeError
    if not self._IsKeyInRange(key):
      raise IndexError
      
    i, j = self._ijKey(key)
    
    row = self._matrix[i]
    element = row[j]
    return copy(element)
  
  def __setitem__(self, key, value):
    """Called to implement matrix[key] = value"""
    if not self._IsValidKey(key):
      raise TypeError
    # if not self._IsValueNumeric(value): TODO
      # raise TypeError 
      
    i, j = self._ijKey(key)
    self._matrix[i][j] = copy(value)
    print self._matrix
    
  def _IsValidKey(self, key):
    """Valid key -> tuple (i, j) where i and j are integers"""
    if InputController.IsTuple(key):
      if not self._IsValidKeyValues(key):
        return False
    else:
      return False
    
    return True
    
  def _IsValidKeyValues(self, key):
    """There has to be two integer values in a tuple."""
    countValues = 0
    for value in key:
      if not InputController.IsInt(value):
        return False
      countValues += 1
    
    if (countValues != 2):
      return False
      
    return True
  
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
      
  def _ijKey(self, key):
    """Transform (rows, columns) -> (1 to n, 1 to m)
       to        (i, j) -> (0 to n-1, 0 to m-1)
       to conform with 0 indexed lists"""
    i = key[0] - 1
    j = key[1] - 1
    return i, j
    
  def __add__(self, other):
    # if not self._IsSameDimension(other): TODO
      # raise Exception(u"Matrices are not of the same dimnsion.")
    matrix = Matrix(self.n_rows, self.m_columns)
    
    for row in range(1, self._CountRows()+1):
      for column in range(1, self._CountColumns()+1):
        matrix[(row, column)] = self._matrix[row-1][column-1] + other[(row, column)]
    return matrix
    
  def __sub__(self, other):
    # if not self._IsSameDimension(other): TODO
      # raise Exception(u"Matrices are not of the same dimnsion.")
    matrix = Matrix(self.n_rows, self.m_columns)
    
    for row in range(1, self._CountRows()+1):
      for column in range(1, self._CountColumns()+1):
        matrix[(row, column)] = self._matrix[row-1][column-1] - other[(row, column)]
    return matrix
    
  def __mul__(self, other):
    """       |
       ---> * |
              V
       """
    
    mulRows, mulColumns = self._GetMulDimensions(other)
    matrix = Matrix(mulRows, mulColumns)
    
    for row in range(1, mulRows+1):
      for column in range(1, mulColumns+1):
        result = self._MulRowWithColumn(self._GetMatrixRow(row), other._GetMatrixColumn(column))
        print result
        matrix[(row, column)] = result
    return matrix
    
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
    
  def transpose(self, other):
    pass
    
  # def __eq__(self, other):
  
  
  # def scale(self, scalar_value):
  
  
  # def __iadd__(self, other):
  
  
  # def __isub__(self, other):
  
  
  # def fromFile(self, path):
  
  
  # def toFile(self, path):
  
    