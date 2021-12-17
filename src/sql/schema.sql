DROP SCHEMA IF EXISTS book_paradise CASCADE;

CREATE SCHEMA IF NOT EXISTS book_paradise;

CREATE TABLE IF NOT EXISTS book_paradise.UserInfo (
    id SERIAL PRIMARY KEY
);

-- Assume that certain book have the same size in all publications for simplicity
CREATE TABLE IF NOT EXISTS book_paradise.Book (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    pages INT NOT NULL CHECK ( pages > 0 ),
    UNIQUE (title, author)
);

CREATE TYPE book_paradise.right_kind as ENUM (
    'see quotes',
    'comment quotes',
    'see portfolio'
);

CREATE TABLE IF NOT EXISTS book_paradise.user_right (
    user_from INT REFERENCES book_paradise.UserInfo,
    user_to INT REFERENCES book_paradise.UserInfo,
    kind book_paradise.right_kind,
    PRIMARY KEY (user_from, user_to, kind)
);

-- User can link book to quote only if he posted this quote, not replied. If quote is replied then book_id will be ignored
CREATE TABLE IF NOT EXISTS book_paradise.Quote (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES book_paradise.UserInfo NOT NULL,
    content TEXT,
    replied_quote_id INT REFERENCES book_paradise.Quote,
    CHECK (
        content IS NULL AND replied_quote_id IS NOT NULL OR
        replied_quote_id IS NULL AND replied_quote_id IS NOT NULL
    ),
    book_id INT REFERENCES book_paradise.Book,
    posted_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS book_paradise.PortfolioBook (
    user_id INT REFERENCES book_paradise.UserInfo,
    book_id INT REFERENCES book_paradise.Book,
    rating INT CHECK ( 0 <= rating AND rating <= 10 ),
    PRIMARY KEY (user_id, book_id)
);

CREATE TABLE IF NOT EXISTS book_paradise.PortfolioRecord (
    user_id INT,
    book_id INT,
    FOREIGN KEY (user_id, book_id) REFERENCES book_paradise.PortfolioBook,
    pages INT NOT NULL CHECK ( pages > 0 ),
    posted_at timestamp DEFAULT NOW(),
    PRIMARY KEY (user_id, book_id, posted_at)
);

CREATE OR REPLACE FUNCTION book_paradise.get_portfolio_intersection(user_id1 INT, user_id2 INT)
    RETURNS book_paradise.Book
    LANGUAGE SQL
AS $$
    WITH intersection_ids AS (
        SELECT ids1.id AS id
        FROM
             (SELECT book_id as id FROM book_paradise.PortfolioBook WHERE user_id = user_id1) ids1 JOIN
             (SELECT book_id as id FROM book_paradise.PortfolioBook WHERE user_id = user_id2) ids2 ON ids1.id = ids2.id
    )
    SELECT *
    FROM book_paradise.Book b
    WHERE b.id IN (SELECT * from intersection_ids)
$$;

CREATE OR REPLACE FUNCTION book_paradise.get_portfolio_statistics(input_user_id INT)
    RETURNS TABLE (book_id INT, read_pages BIGINT, remain_pages BIGINT, wasted_time INT)
    LANGUAGE SQL
AS $$
    SELECT p.book_id as book_id, SUM(p.pages) as read_pages, b.pages - SUM(p.pages) as remain_pages,
           CASE
                WHEN b.pages - SUM(p.pages) = 0 THEN EXTRACT(DAY FROM (MAX(p.posted_at) - MIN(p.posted_at)))::INT
                ELSE EXTRACT(DAY FROM NOW() - MIN(p.posted_at))::INT
           END as wasted_time
    FROM book_paradise.PortfolioRecord p join book_paradise.Book b ON p.book_id = b.id
    WHERE p.user_id = input_user_id
    GROUP BY p.book_id, b.id
$$;
