from psycopg2 import sql





class PostgresSQLConstructor(object):

  def __init__(self, leeked_cursor):
    self.leeked_cursor = leeked_cursor
  
    self._ResetIdentifiers()
    self._ResetData()

    
    
  def GetSQLSelect(self, columns):
    self._SetColumnsIdentifier(columns)
    return "SELECT {columns}"
    
  def GetSQLFrom(self, table):
    self._SetTableIdentifier(table)
    return " FROM {table}"
    
  def GetSQLLimit(self, limit):
    self._SetLimitData(limit)
    return " LIMIT %s"
    
  def GetSQLInsertInto(self, table, columns):
    self._SetTableIdentifier(table)
    self._SetColumnsIdentifier(columns)
    return "INSERT INTO {table} ({columns})"
    
  def GetSQLValues(self, values):
    """["one", "two"] -> (%s, %s)"""
    self._SetInsertValuesData(values)
    length = len(values)
    substitute_string = ", ".join(["%s" for x in range(length)])
    return " VALUES (" + substitute_string + ")"
  
  
  
  def _SetTableIdentifier(self, table):
    self.identifiers["table"] = self._CreateIdentifier(table)
    
  def _SetColumnsIdentifier(self, columns):
    self.identifiers["columns"] = self._JoinSQLIdentifiersWith(columns, ", ")
  
  
  
  def _SetLimitData(self, limit):
    self.data.append(limit)
     
  def _SetInsertValuesData(self, values):
    for value in values:
      self.data.append(value)
  
  
  
  def ApplyIdentifiersToSQL(self, SQL):
    SQL = sql.SQL(SQL).format(**self.identifiers).as_string(self.leeked_cursor)
    self._ResetIdentifiers()
    return SQL
    
  def _ResetIdentifiers(self):
    self.identifiers = {}
    
  def _JoinSQLIdentifiersWith(self, strings, character):
    identifiers = [self._CreateIdentifier(x) for x in strings]
    return sql.SQL(character).join(identifiers)
    
  def _CreateIdentifier(self, identifier):
    return sql.Identifier(identifier)
    
    
    
  def ApplyData(self):
    tuple_data = tuple(self.data)
    self._ResetData()
    return tuple_data
    
  def _ResetData(self):
    self.data = []
    