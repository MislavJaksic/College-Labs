from psycopg2 import sql





class PostgresSQLConstructor(object):
  """
  Constructs SQL statements, takes care of idenifiers and literals.
  """
  def __init__(self, leeked_cursor):
    self.leeked_cursor = leeked_cursor
  
    self._ResetIDs()
    self._ResetLiterals()
    self._ResetCounter()

    
    
  def GetVersion(self):
    return "SELECT version()"
    
  def GetCurrentDate(self):
    return "SELECT current_date"
    
  def GetSELECTColumns(self, columns):
    columns_placeholder = "columns"
    self._SetPlaceholderToValues(columns_placeholder, columns)
    return "SELECT {" + columns_placeholder + "}"
    
  def GetFROMTable(self, table):
    table_placeholder = "table"
    self._SetPlaceholderToValue(table_placeholder, table)
    return " FROM {" + table_placeholder +"}"
    
  def GetLIMIT(self, limit):
    self._SetLiteral(limit)
    return " LIMIT %s"
    
    
    
  def GetINSERTIntoTableColumns(self, table, columns):
    table_placeholder = "table"
    columns_placeholder = "columns"
    self._SetPlaceholderToValue(table_placeholder, table)
    self._SetPlaceholderToValues(columns_placeholder, columns)
    return "INSERT INTO {" + table_placeholder + "} ({" + columns_placeholder +"})"
    
  def GetVALUES(self, values):
    """["one", "two"] -> (%s, %s)"""
    self._SetLiterals(values)
    length = len(values)
    placeholder_string = ", ".join(["%s" for x in range(length)])
    return " VALUES (" + placeholder_string + ")"
    
    
    
  def GetWHERE(self):
    return " WHERE"
    
  def GetAND(self):
    return " AND"
    
  def GetOR(self):
    return " OR"
    
  def GetVectorColumnInQueryPhrase(self, column, phrase):
    column_placeholder = "search_column" + str(self.counter)
    self._SetPlaceholderToValue(column_placeholder, column)
    self._SetLiteral(phrase)
    return " to_TSVector('english', {" + column_placeholder + "}) @@ to_TSQuery('english', %s)"
  
  def ConstructSearchPhrase(self, strings, operator):
    and_phrases = self._AndAllWordsInStrings(strings)
    and_in_brackets_strings = self._SurroundWithBrakcets(and_phrases)
      
    if operator == "AND":
      search_phrases = self._AndAllStrings(and_in_brackets_strings)
    elif operator == "OR":
      search_phrases = self._OrAllStrings(and_in_brackets_strings)
    else:
      print("WARNING: operator has to be either AND or OR")
      
    return search_phrases
      
  def _AndAllWordsInStrings(self, strings):
    return [" & ".join(x.split(" ")) for x in strings]
    
  def _AndAllStrings(self, strings):
    return " & ".join(strings)
  
  def _OrAllStrings(self, strings):
    return " | ".join(strings)
    
  def _SurroundWithBrakcets(self, strings):
    return ["(" + str(x) + ")" for x in strings]
  
  
  
  def _SetPlaceholderToValue(self, placeholder, name):
    self.identifiers[placeholder] = self._CreateID(name)
    self._IncrementCounter()
    
  def _SetPlaceholderToValues(self, placeholder, names):
    self.identifiers[placeholder] = self._JoinSQLIDsWith(names, ", ")
  
  
  
  def _SetLiteral(self, value):
    self.literals.append(value)
     
  def _SetLiterals(self, values):
    for value in values:
      self.literals.append(value)
  
  
  
  def ApplyIDsToSQL(self, SQL):
    print("SQL-->  " + str(SQL))
    print("IDs-->  " + str(self.identifiers))
    SQL = sql.SQL(SQL).format(**self.identifiers).as_string(self.leeked_cursor)
    self._ResetIDs()
    self._ResetCounter()
    return SQL
    
  def _ResetIDs(self):
    self.identifiers = {}
    
  def _JoinSQLIDsWith(self, strings, character):
    identifiers = [self._CreateID(x) for x in strings]
    return sql.SQL(character).join(identifiers)
    
  def _CreateID(self, identifier):
    return sql.Identifier(identifier)
    
    
    
  def ApplyLiterals(self):
    print("Literals-->  " + str(self.literals))
    tuple_literals = tuple(self.literals)
    self._ResetLiterals()
    return tuple_literals
    
  def _ResetLiterals(self):
    self.literals = []
    
    
  
  def _ResetCounter(self):
    self.counter = 0
    
  def _IncrementCounter(self):
    self.counter = self.counter + 1
    