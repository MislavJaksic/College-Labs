CREATE TABLE queries (
    query_id bigserial primary key,
    query character varying(255) not null,
    date_and_time timestamp not null
);

INSERT INTO queries (query, date_and_time) VALUES ('SELECT * FROM imaginary_table;', '1999-01-08 04:05:06');