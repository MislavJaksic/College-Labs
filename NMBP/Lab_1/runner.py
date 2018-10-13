from PostgresManager import PostgresManager





if __name__ == '__main__':
  with PostgresManager() as postgres:
    print(postgres.SelectColumnsFromTable(["movie_id", "title"], "movies", 5))
    print(postgres.DescribeTable("movies"))
    print(postgres.InsertIntoMovies("Hello, this is a test: is everything ok?"))
  
  
  
  """
  SELECT alias, description, token
FROM ts_debug ('english',
'The Dancing Ladies');
  """