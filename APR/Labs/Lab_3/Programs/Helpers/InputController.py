import types

class InputController(object):
  @staticmethod
  def IsDict(param):
    """Checks if the paramater is a dictionary."""
    if type(param) is types.DictType:
      return True
    return False

  @staticmethod
  def IsBool(param):
    """Checks if the paramater is a boolean value."""
    if type(param) is types.BooleanType:
      return True
    return False
    
  @staticmethod
  def IsList(param):
    """Checks if the paramater is a list."""
    if type(param) is types.ListType:
      return True
    return False
  
  @staticmethod
  def IsString(param):
    """Checks if the paramater is a string."""
    if type(param) is types.StringType:
      return True
    return False
    
  @staticmethod
  def IsTuple(param):
    """Checks if the paramater is a list."""
    if type(param) is types.TupleType:
      return True
    return False
  
  @staticmethod
  def IsInt(param):
    """Checks if the paramater is an integer."""
    if type(param) is types.IntType:
      return True
    return False
    
  @staticmethod
  def IsLong(param):
    """Checks if the paramater is an integer."""
    if type(param) is types.LongType:
      return True
    return False
  
  @staticmethod
  def IsFloat(param):
    """Checks if the paramater is a floating point number."""
    if type(param) is types.FloatType:
      return True
    return False