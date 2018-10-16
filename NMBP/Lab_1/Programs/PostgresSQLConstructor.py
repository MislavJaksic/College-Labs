from psycopg2 import sql





class PostgresSQLConstructor(object):
  """
  Constructs SQL statements, takes care of idenifiers and literals.
  """
  def __init__(self):
    pass
    
    
  def GetVersion(self):
    return "SELECT version()"
    
  def GetCurrentDate(self):
    return "SELECT current_date"
   

   
  def GetSELECTColumns(self, columns):
    return "SELECT " + ", ".join(columns)
    
  def GetFROMTable(self, table):
    return " FROM " + table
    
  def GetLIMIT(self, limit):
    return " LIMIT " + str(limit)
    
  def GetWHERE(self):
    return " WHERE"
    
  def GetAND(self):
    return " AND"
    
  def GetOR(self):
    return " OR"
  
  def GetORDERByAliasInDirection(self, alias, direction="ASC"):
    return " ORDER BY " + alias + " " + direction
    
    
  
  def GetHeadlineColumnsWithPhrase(self, columns, phrase):
    headlined_columns = []
    for column in columns:
      headlined_columns.append("ts_headline(" + column + "," + self.Getto_TSQueryPhrase(phrase) + ")")
      
    return headlined_columns
  
  def Getts_rankColumnByPhraseWithLengthPenaltyWithAlias(self, column, phrase, penalty=1, alias="rank"):
    if penalty not in (0,1,2,4,8,16,32):
      raise Exception("WARNING: incorrect penalty; possible penalties are 0,1,2,4,8,16,32")
      
    return "ts_rank(" + self.Getto_TSVectorColumn(column) + "," + self.Getto_TSQueryPhrase(phrase) + ", " + str(penalty) + ") as " + alias
  
  def Getts_rankDocumentByPhraseWithLengthPenaltyWithAlias(self, document, phrase, penalty=1, alias="rank"):
    if penalty not in (0,1,2,4,8,16,32):
      raise Exception("WARNING: incorrect penalty; possible penalties are 0,1,2,4,8,16,32")
      
    return "ts_rank(" + document + "," + self.Getto_TSQueryPhrase(phrase) + ", " + str(penalty) + ") as " + alias
  
  def GetVectorColumnHasQueryPhrase(self, column, phrase):
    return self.Getto_TSVectorColumn(column) + self.GetFTSOperator() + self.Getto_TSQueryPhrase(phrase)
    
  def GetDocumentHasQueryPhrase(self, document, phrase):
    return " " + document + self.GetFTSOperator() + self.Getto_TSQueryPhrase(phrase)
    
  def Getto_TSVectorColumn(self, column):
    return " to_TSVector('english', " + column + ")"
    
  def GetFTSOperator(self):
    return " @@"
    
  def Getto_TSQueryPhrase(self, phrase):
    single_quoted_phrase = "'" + phrase + "'"
    return " to_TSQuery('english', " + single_quoted_phrase + ")"
  
  def GetSimilarityOfColumnAndStringWithAlias(self, column, string, alias="sameness"):
    single_quoted_string = "'" + string + "'"
    return " similarity(" + column + ", " + single_quoted_string + ") as " + alias
  
  
  def ConstructSearchPhrase(self, strings, operator):
    and_phrases = self._AndAllWordsInStrings(strings)
    and_in_brackets_strings = self._SurroundWithBrakcets(and_phrases)
      
    if operator == "AND":
      search_phrases = self._AndAllStrings(and_in_brackets_strings)
    elif operator == "OR":
      search_phrases = self._OrAllStrings(and_in_brackets_strings)
    else:
      raise Exception("WARNING: operator has to be either AND or OR")
      
    return search_phrases
      
  def _AndAllWordsInStrings(self, strings):
    return [" & ".join(x.split(" ")) for x in strings]
    
  def _AndAllStrings(self, strings):
    return " & ".join(strings)
  
  def _OrAllStrings(self, strings):
    return " | ".join(strings)
    
  def _SurroundWithBrakcets(self, strings):
    return ["(" + str(x) + ")" for x in strings]
  


  def GetINSERTIntoTableColumns(self, table, columns):
    return "INSERT INTO " + table + " (" + ", ".join(columns) +")"
    
  def GetVALUES(self, values):
    single_quoted_values = ["'" + x + "'" for x in values]
    return " VALUES (" + ", ".join(single_quoted_values) + ")"
