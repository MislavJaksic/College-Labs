CREATE EXTENSION IF NOT EXISTS fuzzystrmatch; -- (soundex, levenshtein, metaphone)
CREATE EXTENSION IF NOT EXISTS pg_trgm; -- (similarity , show_Trgm,…, %, <->)
CREATE EXTENSION IF NOT EXISTS tablefunc; -- (crosstab)
CREATE EXTENSION IF NOT EXISTS ltree; -- (ltree)