from PostgresQuerier import PostgresQuerier





class PostgresManager(object):

  def __init__(self):
    pass
  
  def __enter__(self):
    self.querier = PostgresQuerier()
    return self.querier
  
  def __exit__(self, exc_type, exc_value, traceback):
    self.querier.Close()
    