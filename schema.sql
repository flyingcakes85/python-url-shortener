DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id INTEGER PRIMARY KEY,
    shortcode TEXT NOT NULL,
    redirect TEXT NOT NULL
);