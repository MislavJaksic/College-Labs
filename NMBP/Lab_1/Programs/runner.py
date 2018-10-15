from PostgresManager import PostgresManager





TABLE_NAME = "movies"
COLUMN_NAMES = ["movie_id", "title", "categories", "summary", "description"]

if __name__ == '__main__':
  with PostgresManager() as postgres:
    print(postgres.GetCurrentDate())
    print(postgres.DescribeTable("movies"))
    print(postgres.SelectColumnsFromTable(["title"], "movies", 5))
    print(postgres.InsertIntoMovies("Test insertion. Pay no attention to it."))
    print(postgres.FindWordsInColumnsInTable(["Legend of", "Lord of", "Dance", "Ancient Japan"], ["description", "title"], "movies", operation="OR"))
    print(postgres.SuggestWordInColumnInTable("sudent", "summary", "movies"))
    #print(postgres.Prototype())
  
  
  """
  SELECT alias, description, token
FROM ts_debug ('english',
'The Dancing Ladies');
  """