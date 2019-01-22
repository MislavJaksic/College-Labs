import dateutil
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
    
  def FindWordsInColumnsInTableThenBoldAndRank(self, search_words, columns, table, operation="OR"):
    search_phrase = self.SQL_constructor.ConstructSearchPhrase(search_words, operation)
    
    headline_columns = self.SQL_constructor.GetHeadlineColumnsWithPhrase(columns, search_phrase)
    rank_column = self.SQL_constructor.Getts_rankColumnByPhraseWithLengthPenaltyWithAlias(columns[0], search_phrase, 1, "rank")
    headline_columns.append(rank_column)
    
    vector_query_pairs = [self.SQL_constructor.GetVectorColumnHasQueryPhrase(x, search_phrase) for x in columns]
    
    SQL_select = self.SQL_constructor.GetSELECTColumns(headline_columns)
    SQL_from = self.SQL_constructor.GetFROMTable(table)
    SQL_where = self.SQL_constructor.GetWHERE()
    SQL_conditions = " OR".join(vector_query_pairs)
    SQL_order = self.SQL_constructor.GetORDERByAliasInDirection("rank", "DESC")

    SQL = SQL_select + SQL_from + SQL_where + SQL_conditions + SQL_order
    
    self.connector.ExecuteSQL(SQL)
    return self.connector.GetAllResults()
  
  def FindWordsInDocumentInTableThenBoldAndRank(self, search_words, document, table, operation="OR"):
    search_phrase = self.SQL_constructor.ConstructSearchPhrase(search_words, operation)
    document_columns = ["title", "categories", "summary", "description"]
    
    headline_columns = self.SQL_constructor.GetHeadlineColumnsWithPhrase(document_columns, search_phrase)
    rank_column = self.SQL_constructor.Getts_rankDocumentByPhraseWithLengthPenaltyWithAlias(document, search_phrase, 1, "rank")
    
    headline_columns.append(rank_column)
    
    SQL_select = self.SQL_constructor.GetSELECTColumns(headline_columns)
    SQL_from = self.SQL_constructor.GetFROMTable(table)
    SQL_where = self.SQL_constructor.GetWHERE()
    SQL_conditions = self.SQL_constructor.GetDocumentHasQueryPhrase(document, search_phrase)
    SQL_order = self.SQL_constructor.GetORDERByAliasInDirection("rank", "DESC")
    
    SQL = SQL_select + SQL_from + SQL_where + SQL_conditions + SQL_order
    
    self.connector.ExecuteSQL(SQL)
    return self.connector.GetAllResults()
    
    
    
  def SuggestBasedOnPhraseInColumnInTable(self, phrase, column, table):
    similarity_function = self.SQL_constructor.GetSimilarityOfColumnAndStringWithAlias(column, phrase, "sameness")
    
    SQL_select = self.SQL_constructor.GetSELECTColumns([column, similarity_function])
    SQL_from = self.SQL_constructor.GetFROMTable(table)
    SQL_order = self.SQL_constructor.GetORDERByAliasInDirection("sameness", "DESC")
    
    SQL = SQL_select + SQL_from + SQL_order
    
    self.connector.ExecuteSQL(SQL)
    return self.connector.GetResults(5)
  


  def PivotMovies(self, start_datetime, stop_datetime, granulation):
    iso_start_datetime = start_datetime.isoformat(" ")
    iso_end_datetime = stop_datetime.isoformat(" ")
    
    diff = stop_datetime - start_datetime
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    
    if granulation == "hour":
      format = ["time_interval" + str(x) + " bigint" for x in range(hours + 1)]
    elif granulation == "day":
      format = ["time_interval" + str(x) + " bigint" for x in range(days + 1)]
    else:
      raise Exception("WARNING: incorrect granulation; possible granulation are (hour, day)")
    
    format.insert(0, "query character varying(255)")
    
    sub_query = ("select query,"
                 " date_trunc(''" + granulation + "'', date_and_time) as periods,"
                 " count(*)"
                 " from queries"
                 " where date_and_time >= ''" + iso_start_datetime + "'' and"
                       " date_and_time <= ''" + iso_end_datetime + "''"
                 " group by query, periods"
                 " order by query, periods;")
    sequence = ("select d"
                " from generate_series(''" + iso_start_datetime + "''::timestamp,"
                                      "''" + iso_end_datetime + "'',"
                                      "''1 " + granulation + "'')"
                " d;")
    SQL = ("select * from crosstab('" + sub_query + "',"
                                  "'" + sequence + "')"
           "as ct(" + ", ".join(format) + ");")
           
    self.connector.ExecuteSQL(SQL)
    return self.connector.GetAllResults()
                 
    
    
  def InsertIntoMovies(self, title, categories="No categories.", summary="No summary.", description="No description."):
    table = "movies"
    columns = ["title", "categories", "summary", "description"]
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
