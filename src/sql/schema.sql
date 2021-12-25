DROP SCHEMA IF EXISTS book_paradise CASCADE;

CREATE SCHEMA IF NOT EXISTS book_paradise;

CREATE TABLE IF NOT EXISTS book_paradise.UserInfo (
    id SERIAL PRIMARY KEY,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
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

CREATE TABLE IF NOT EXISTS book_paradise.UserRight (
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
        replied_quote_id IS NULL AND content IS NOT NULL
    ),
    book_id INT REFERENCES book_paradise.Book,
    posted_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS book_paradise.QuoteComment (
    id SERIAL PRIMARY KEY,
    quote_id INT REFERENCES book_paradise.Quote NOT NULL,
    posted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    user_id INT REFERENCES book_paradise.UserInfo NOT NULL,
    content TEXT NOT NULL
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

WITH pwd AS (
    SELECT generate_series(1, 3) AS id,  UNNEST(ARRAY['$2b$12$KTguiTfEL.o3RmgyRGSASOK9ycaAMMjkiWLJbeSWGDdEwbAlG20rG', -- secret
        '$2b$12$Akpcvgq7rW1wzSs9zaAMhuMWbQ7HbjV.u5bSk6B70pEtsL2pYp4XC', -- superpassword
        '$2b$12$hU2X49aYYdNL58s.cwm5MORsi83aLsWXLwK1OzzyIR46UA.Nftavq']) AS pwd -- password
), logins AS (
    SELECT generate_series(1, 3) AS id, UNNEST(ARRAY['sam-victor', 'victor', 'sam']) as log
)
INSERT INTO book_paradise.UserInfo(login, password)
SELECT log, pwd
FROM pwd JOIN logins ON pwd.id = logins.id;

INSERT INTO book_paradise.Book(title, author, pages)
SELECT title, author, (700 * random())::INTEGER
FROM (
    SELECT unnest(ARRAY['Война и мир', '1984', 'Улисс', 'Лолита', 'Звук и ярость', 'Человек-невидимка', 'На маяк', 'Илиада', 'Одиссея', 'Божественная комедия']) AS title,
           unnest(ARRAY['Лев Толстой', 'Джордж Оруэлл', 'Джеймс Джойс', 'Владимир Набоков', 'Уильям Фолкнер', 'Ральф Эллисон', 'Вирджиния Вулф', 'Гомер', 'Гомер', 'Данте Алигьери']) AS author
) as ta;

INSERT INTO book_paradise.UserRight(user_from, user_to, kind)
SELECT 1, 2, k.kind
FROM (SELECT unnest(enum_range(NULL::book_paradise.right_kind)) as kind) as k
