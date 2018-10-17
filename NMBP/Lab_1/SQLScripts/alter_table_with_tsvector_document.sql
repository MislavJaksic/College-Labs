ALTER TABLE movies ADD COLUMN TSVector_document tsvector;
UPDATE movies SET TSVector_document = to_TSVector('english', coalesce(title, '') || ' ' ||
                                                             coalesce(categories, '') || ' ' ||
                                                             coalesce(summary, '') || ' ' ||
                                                             coalesce(description, ''));