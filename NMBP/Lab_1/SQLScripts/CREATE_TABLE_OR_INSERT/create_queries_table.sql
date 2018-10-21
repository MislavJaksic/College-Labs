CREATE TABLE queries (
    query_id bigserial primary key,
    query character varying(255) not null,
    date_and_time timestamp not null
);

INSERT INTO queries (query, date_and_time) VALUES ('SELECT * FROM imaginary_table;', '1999-01-08 04:05:06');
INSERT INTO queries (query, date_and_time) VALUES ("SELECT * FROM imaginary_table;", "1999-01-10 04:05:06");
INSERT INTO queries (query, date_and_time) VALUES ("SELECT * FROM imaginary_table;", "1999-01-11 04:05:06");
INSERT INTO queries (query, date_and_time) VALUES ("SELECT * FROM imaginary_table;", "1999-01-11 06:05:06");
INSERT INTO queries (query, date_and_time) VALUES ("SELECT * FROM imaginary_table;", "1999-01-11 07:05:06");
INSERT INTO queries (query, date_and_time) VALUES ("SELECT * FROM imaginary_table;", "1999-01-11 10:05:06");
INSERT INTO queries (query, date_and_time) VALUES ("SELECT a_column FROM another_table;", "1999-01-09 05:05:06");
INSERT INTO queries (query, date_and_time) VALUES ("SELECT a_column FROM another_table;", "1999-01-11 09:05:06");
INSERT INTO queries (query, date_and_time) VALUES ("SELECT a_column FROM another_table;", "1999-01-10 08:05:06");

