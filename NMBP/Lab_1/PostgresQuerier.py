from PostgresConnector import PostgresConnector
from PostgresSQLConstructor import PostgresSQLConstructor





CONFIG_FILE_NAME = "database.ini"
CONFIG_SECTION_NAME = "postgresql"

class PostgresQuerier(object):
  
  def __init__(self):
    self.connector = PostgresConnector(CONFIG_FILE_NAME, CONFIG_SECTION_NAME)
    self.SQL_constructor = PostgresSQLConstructor(self.connector._LeekCursor())
  

    
  def GetVersion(self):
    SQL = self.SQL_constructor.GetVersion()
    self.connector.ExecuteSQL(SQL)
    return self.connector.GetResults(1)
    
  def GetCurrentDate(self):
    SQL = self.SQL_constructor.GetCurrentDate()
    self.connector.ExecuteSQL(SQL)
    return self.connector.GetResults(1)
    
  def _SetDatestyleGerman(self):
    SQL = "SET DATESTYLE=%s;";
    data = ("German",)
    self.connector.ExecuteSQL(SQL, data)
    return "Datestyle set to German"
    
  def DescribeTable(self, table):
    SQL = "SELECT column_name FROM information_schema.columns WHERE table_name = %s";
    data = (table,)
    self.connector.ExecuteSQL(SQL, data)
    return self.connector.GetAllResults()
    
  def SelectColumnsFromTable(self, columns, table, limit=100):
    SQL_select = self.SQL_constructor.GetSELECTColumns(columns)
    SQL_from = self.SQL_constructor.GetFROMTable(table)
    SQL_limit = self.SQL_constructor.GetLIMIT(limit)

    SQL = self.SQL_constructor.ApplyIDsToSQL(SQL_select + SQL_from + SQL_limit)
    data = self.SQL_constructor.ApplyLiterals()
    
    self.connector.ExecuteSQL(SQL, data)
    return self.connector.GetAllResults()
    
  def FindInMovies(self, search_words, operation):
    table = "movies"
    columns = self._GetTableColumnsAfter(table, 1)
    
    SQL_select = self.SQL_constructor.GetSELECTColumns(columns)
    SQL_from = self.SQL_constructor.GetFROMTable(table)
    
    search_phrase = self.SQL_constructor.ConstructSearchPhrase(search_words, operation)
    vector_query_pairs = [self.SQL_constructor.GetVectorColumnInQueryPhrase(x, search_phrase) for x in columns]
    
    SQL_where = self.SQL_constructor.GetWHERE()
    SQL_conditions = " OR".join(vector_query_pairs)
    
    SQL = SQL_select + SQL_from + SQL_where + SQL_conditions
    
    SQL = self.SQL_constructor.ApplyIDsToSQL(SQL)
    data = self.SQL_constructor.ApplyLiterals()
    
    self.connector.ExecuteSQL(SQL, data)
    return self.connector.GetAllResults()
    
    
    
  def InsertIntoMovies(self, title, categories="No categories.", summary="No summary.", description="No description."):
    table = "movies"
    columns = self._GetTableColumnsAfter(table, 1)
    values = [title, categories, summary, description]
    
    SQL_insert = self.SQL_constructor.GetINSERTIntoTableColumns(table, columns)
    SQL_values = self.SQL_constructor.GetVALUES(values)
    
    SQL = SQL_insert + SQL_values
    
    SQL = self.SQL_constructor.ApplyIDsToSQL(SQL)
    data = self.SQL_constructor.ApplyLiterals()
    
    self.connector.ExecuteSQL(SQL, data)
    self.connector.CommitTransaction()
    return "Insertion successful."
  
  def _GetTableColumnsAfter(self, table, index=0):
    return [x[0] for x in self.DescribeTable(table)][index:]

  
  
  def Close(self):
    self.connector.Close()
