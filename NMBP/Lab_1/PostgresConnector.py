from configparser import ConfigParser
import psycopg2



class PostgresConnector(object):
  
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
  
  def _LeekCursor(self):
    return self.cursor
  
  
  
  def ExecuteCommandOrSQL(self, command_or_SQL, data=()):
    try:
      self.cursor.execute(command_or_SQL, data)
      print("Executed--->  " + command_or_SQL)
    except (Exception) as error:
      print(error)
      self.Close()
      
  def GetResults(self, number):
    results = None
    try:
      results = self.cursor.fetchmany(number)
    except (Exception) as error:
      print(error)
      self.Close()
    if results is not None:
      print("Results-->  " + str(results[0]) + "...")
    return results
  
  def GetAllResults(self):
    results = None
    try:
      results = self.cursor.fetchall()
    except (Exception) as error:
      print(error)
      self.Close()
    if results is not None:
      print("Results-->  " + str(results[0]) + "...")
    return results
  
  def CommitTransaction(self):
    self.connection.commit()
  
  
  
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
