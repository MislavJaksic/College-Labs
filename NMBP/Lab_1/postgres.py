from configparser import ConfigParser
import psycopg2
from psycopg2 import sql

CONFIG_FILE_NAME = "database.ini"
CONFIG_SECTION_NAME = "postgresql"



class PostgresWrapper(object):
  
  def __init__(self, config_file_name, config_section_name):
    self.config_file_name = config_file_name
    self.config_section_name = config_section_name
    self.config = self._LoadConfiguration()
    
    self.connection = None
    self.cursor = None
    self.connection = self._CreateConnection()
    self.cursor = self._CreateCursor()
  
  def _LoadConfiguration(self):
    self.config_file = self._ParseConfigFile()
    config = self._ReadConfigFromConfigFile()
    return config
  
  def _ParseConfigFile(self):
    parser = ConfigParser()
    try:
      parser.read(self.config_file_name)
    except (Exception) as error:
      raise Exception("Configuration file {0} not found".format(self.config_file_name))
    return parser
    
  def _ReadConfigFromConfigFile(self):
    config = {}
    if self.config_file.has_section(self.config_section_name):
      key_value_pairs = self.config_file.items(self.config_section_name)
      for key_value in key_value_pairs:
        key = key_value[0]
        value = key_value[1]
        config[key] = value
    else:
      raise Exception("Section {0} not found".format(self.config_section_name))
    return config

    
    
  def _CreateConnection(self):
    connection = None
    print('Connecting to the PostgreSQL database...')
    try:
      connection = psycopg2.connect(**self.config)
    except (Exception) as error:
      print(error)
    return connection
    
  def _CreateCursor(self):
    cursor = None
    try:
      cursor = self.connection.cursor()
    except (Exception) as error:
      print(error)
      self._CloseConnection()
    return cursor
    
    
    
  def GetVersion(self):
    SQL = "SELECT version();"
    self._ExecuteCommandOrSQL(SQL)
    return self._GetResults(1)
    
  def GetCurrentDate(self):
    SQL = "SELECT current_date;"
    self._ExecuteCommandOrSQL(SQL)
    return self._GetResults(1)
    
  def _SetDatestyleGerman(self):
    SQL = "SET DATESTYLE=%s;";
    data = ("German",)
    self._ExecuteCommandOrSQL(SQL, data)
    return "Datestyle set to German"
    
  def DescribeTable(self, table):
    #command = "\d+ %s" META COMMAND DON?T WORK
    SQL = "SELECT column_name FROM information_schema.columns WHERE table_name = %s";
    data = (table,)
    self._ExecuteCommandOrSQL(SQL, data)
    return self._GetAllResults()
    
  def SelectColumnsFromTable(self, columns, table, limit=None): TODO
    SQL = "SELECT {select} FROM {from}"
    if limit is not None:
      SQL = SQL + " LIMIT %s"
      data = (limit,)
      
    SQL = self._ConstructSelectFrom(SQL, columns, table)
    print(SQL)
    self._ExecuteCommandOrSQL(SQL, data)
    return self._GetAllResults()
    
  def _ConstructSelectFrom(self, statement, columns, table): TODO
    identifiers = {"select" : self._JoinIdentifiersWith(columns, ", "),
                   "from" : sql.Identifier(table),
                  }
    print(sql.SQL(statement).format(**identifiers))
    return sql.SQL(statement).format(**identifiers)
    
  def _JoinIdentifiersWith(self, identifiers, character): TODO
    formatted_identifiers = [sql.Identifier(x) for x in identifiers]
    print(sql.SQL(character).join(formatted_identifiers))
    return sql.SQL(character).join(formatted_identifiers)
    
  def _CreateIdentifier(self, identifier):
    return sql.Indentifier(identifier);
    
    
    
  def _ExecuteCommandOrSQL(self, SQL_or_command, data=[]):
    try:
      self.cursor.execute(SQL_or_command, data)
      print("Executed--->  " + SQL_or_command)
    except (Exception) as error:
      print(error)
      self.Close()
      
  def _GetResults(self, number):
    results = None
    try:
      results = self.cursor.fetchmany(number)
    except (Exception) as error:
      print(error)
      self.Close()
    if results is not None:
      print("Results-->  " + str(results[0]) + "...")
    return results
  
  def _GetAllResults(self):
    results = None
    try:
      results = self.cursor.fetchall()
    except (Exception) as error:
      print(error)
      self.Close()
    if results is not None:
      print("Results-->  " + str(results[0]) + "...")
    return results
  
  
  def Close(self):
    self._CloseConnection()
    self._CloseCursor()
    
  def _CloseConnection(self):
    if self.connection is not None:
      self.connection.close()
      print("Connection closed")
      
  def _CloseCursor(self):
    if self.cursor is not None:
      self.cursor.close()
      print("Cursor closed")

      
      
      
      
if __name__ == '__main__':
  postgres = PostgresWrapper(CONFIG_FILE_NAME, CONFIG_SECTION_NAME)
  print(postgres.GetVersion())
  print(postgres.GetCurrentDate())
  print(postgres.DescribeTable("movie"))
  print(postgres.SelectColumnsFromTable(["movieid", "title"], "movie", 20))
  postgres.Close()
  
  SQL_string = "select {one} from {two}"
  data = {"one" : sql.Identifier("hello"), "two" : sql.Identifier("world")}
  print(sql.SQL(SQL_string).format(**data))
  
  """
  SELECT alias, description, token
FROM ts_debug ('english',
'The Dancing Ladies');
  """
  
  
  
  
