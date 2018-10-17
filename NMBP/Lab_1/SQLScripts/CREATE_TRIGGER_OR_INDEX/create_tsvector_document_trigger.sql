CREATE FUNCTION document_trigger() RETURNS trigger AS $$
begin
  new.TSVector_document :=
    setweight(to_tsvector('english', coalesce(new.title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(new.categories, '')), 'B') ||
    setweight(to_tsvector('english', coalesce(new.summary, '')), 'C') ||
    setweight(to_tsvector('english', coalesce(new.description, '')), 'D');
  return new;
end
$$ LANGUAGE plpgsql;
CREATE TRIGGER TSVector_document_update BEFORE INSERT OR UPDATE
ON movies FOR EACH ROW EXECUTE PROCEDURE document_trigger();