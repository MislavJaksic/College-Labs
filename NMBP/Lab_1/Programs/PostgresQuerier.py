from PostgresConnector import PostgresConnector
from PostgresSQLConstructor import PostgresSQLConstructor





CONFIG_FILE_NAME = "database.ini"
CONFIG_SECTION_NAME = "postgresql"

class PostgresQuerier(object):
  
  def __init__(self):
    self.connector = PostgresConnector(CONFIG_FILE_NAME, CONFIG_SECTION_NAME)
    self.SQL_constructor = PostgresSQLConstructor()
  

    
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
    
  
    
  def SelectColumnsFromTable(self, columns, table, limit=100):
    SQL_select = self.SQL_constructor.GetSELECTColumns(columns)
    SQL_from = self.SQL_constructor.GetFROMTable(table)
    SQL_limit = self.SQL_constructor.GetLIMIT(limit)

    SQL = SQL_select + SQL_from + SQL_limit
    
    self.connector.ExecuteSQL(SQL)
    return self.connector.GetAllResults()
    
  def FindWordsInColumnsInTable(self, search_words, columns, table, operation="OR"):
    search_phrase = self.SQL_constructor.ConstructSearchPhrase(search_words, operation)
    
    headline_columns = self.SQL_constructor.GetHeadlineColumnsWithPhrase(columns, search_phrase)
    rank_column = self.SQL_constructor.Getts_rankColumnByPhraseWithLengthPenaltyWithAlias(columns[0], search_phrase, 1, "rank")
    
    headline_columns.append(rank_column)
    
    SQL_select = self.SQL_constructor.GetSELECTColumns(headline_columns)
    SQL_from = self.SQL_constructor.GetFROMTable(table)
    SQL_where = self.SQL_constructor.GetWHERE()
    SQL_order = self.SQL_constructor.GetORDERByAliasInDirection("rank", "DESC")
    
    vector_query_pairs = [self.SQL_constructor.GetVectorColumnHasQueryPhrase(x, search_phrase) for x in columns]
    SQL_conditions = " OR".join(vector_query_pairs)
    
    SQL = SQL_select + SQL_from + SQL_where + SQL_conditions + SQL_order
    
    self.connector.ExecuteSQL(SQL)
    return self.connector.GetAllResults()
    
    
    
  def SuggestWordInColumnInTable(self, word, column, table):
    similarity_function = self.SQL_constructor.GetSimilarityOfColumnAndStringWithAlias(column, word, "sameness")
    
    SQL_select = self.SQL_constructor.GetSELECTColumns([column, similarity_function])
    SQL_from = self.SQL_constructor.GetFROMTable(table)
    SQL_order = self.SQL_constructor.GetORDERByAliasInDirection("sameness", "DESC")
    
    SQL = SQL_select + SQL_from + SQL_order
    
    self.connector.ExecuteSQL(SQL)
    return self.connector.GetResults(5)
    
    
    
  def InsertIntoMovies(self, title, categories="No categories.", summary="No summary.", description="No description."):
    table = "movies"
    columns = self._GetTableColumnsAfterIndex(table, 1)
    values = [title, categories, summary, description]
    
    SQL_insert = self.SQL_constructor.GetINSERTIntoTableColumns(table, columns)
    SQL_values = self.SQL_constructor.GetVALUES(values)
    
    SQL = SQL_insert + SQL_values
    
    self.connector.ExecuteSQL(SQL)
    self.connector.CommitTransaction()
    return "Insertion successful."
  
  def _GetTableColumnsAfterIndex(self, table, index=0):
    return [x[0] for x in self.DescribeTable(table)][index:]
  
  
  
  def Prototype(self):
    SQL = ("SELECT title, similarity (title, 'The Dencing Master')"
           "FROM movies"
           "WHERE title % 'The Dencing Master'"
           )
    self.connector.ExecuteSQL(SQL)
    return self.connector.GetAllResults()
    
    
    
  def DescribeTable(self, table):
    SQL = "SELECT column_name FROM information_schema.columns WHERE table_name = '" + table + "'";
    self.connector.ExecuteSQL(SQL)
    return self.connector.GetAllResults()
  
  
  
  def Close(self):
    self.connector.Close()
