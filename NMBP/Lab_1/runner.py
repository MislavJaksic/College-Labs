from PostgresManager import PostgresManager





if __name__ == '__main__':
  with PostgresManager() as postgres:
    print(postgres.GetCurrentDate())
    print(postgres.DescribeTable("movies"))
    print(postgres.SelectColumnsFromTable(["title"], "movies", 5))
    print(postgres.InsertIntoMovies("Test insertion. Pay no attention to it."))
    print(postgres._Cheat())
    print(postgres.FindInMovies(["Legend of", "Lord of", "Dance"], "OR"))
  
  
  
  """
  SELECT alias, description, token
FROM ts_debug ('english',
'The Dancing Ladies');
  """