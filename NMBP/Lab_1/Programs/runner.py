from PostgresManager import PostgresManager





TABLE_NAME = "movies"
COLUMN_NAMES = ["movie_id", "title", "categories", "summary", "description", "tsvector_document"]

if __name__ == '__main__':
  with PostgresManager() as postgres:
    print(postgres.GetCurrentDate())
    print(postgres.DescribeTable("movies"))
    print(postgres.SelectColumnsFromTable(["title"], "movies", 5))
    print(postgres.InsertIntoMovies("Test insertion. Pay no attention to it."))
    print(postgres.FindWordsInColumnsInTableThenBoldAndRank(["Dance", "Ancient Japan"], ["title", "summary"], "movies", operation="OR"))
    print(postgres.SuggestBasedOnPhraseInColumnInTable("sudent", "summary", "movies"))
    
    print(postgres.FindWordsInDocumentInTableThenBoldAndRank(["Dance", "Ancient Japan"], "tsvector_document", "movies", operation="OR"))
    #print(postgres.Prototype())
  