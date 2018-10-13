from PostgresConnector import PostgresConnector
from PostgresSQLConstructor import PostgresSQLConstructor





CONFIG_FILE_NAME = "database.ini"
CONFIG_SECTION_NAME = "postgresql"

class PostgresQuerier(object):
  
  def __init__(self):
    self.connector = PostgresConnector(CONFIG_FILE_NAME, CONFIG_SECTION_NAME)
    self.SQL_constructor = PostgresSQLConstructor(self.connector._LeekCursor())
  

    
  def GetVersion(self):
    SQL = "SELECT version();"
    self.connector.ExecuteCommandOrSQL(SQL)
    return self.connector.GetResults(1)
    
  def GetCurrentDate(self):
    SQL = "SELECT current_date;"
    self.connector.ExecuteCommandOrSQL(SQL)
    return self.connector.GetResults(1)
    
  def _SetDatestyleGerman(self):
    SQL = "SET DATESTYLE=%s;";
    data = ("German",)
    self.connector.ExecuteCommandOrSQL(SQL, data)
    return "Datestyle set to German"
    
  def DescribeTable(self, table):
    #command = "\d+ %s" META COMMAND DON?T WORK
    SQL = "SELECT column_name FROM information_schema.columns WHERE table_name = %s";
    data = (table,)
    self.connector.ExecuteCommandOrSQL(SQL, data)
    return self.connector.GetAllResults()
    
  def SelectColumnsFromTable(self, columns, table, limit=100):
    SQL = self.SQL_constructor.GetSQLSelect(columns) + self.SQL_constructor.GetSQLFrom(table) + self.SQL_constructor.GetSQLLimit(limit)
    
    SQL = self.SQL_constructor.ApplyIdentifiersToSQL(SQL)
    data = self.SQL_constructor.ApplyData()
    
    self.connector.ExecuteCommandOrSQL(SQL, data)
    return self.connector.GetAllResults()
    
    
    
  def InsertIntoMovies(self, title, categories="No categories.", summary="No summary.", description="No description."):
    table = "movies"
    data_columns = [x[0] for x in self.DescribeTable(table)][1:]
    values = [title, categories, summary, description]
    SQL = self.SQL_constructor.GetSQLInsertInto(table, data_columns) + self.SQL_constructor.GetSQLValues(values)
    
    SQL = self.SQL_constructor.ApplyIdentifiersToSQL(SQL)
    data = self.SQL_constructor.ApplyData()
    
    self.connector.ExecuteCommandOrSQL(SQL, data)
    self.connector.CommitTransaction()
    return self.connector.GetAllResults()
    
  
  
  def Close(self):
    self.connector.Close()
