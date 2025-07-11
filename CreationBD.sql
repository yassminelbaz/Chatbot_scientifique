 -- Créer la base de données
CREATE DATABASE IF NOT EXISTS chatbot_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE chatbot_db ;

-- Table articles
CREATE TABLE IF NOT EXISTS articles (
    id_article VARCHAR(50) PRIMARY KEY,
    title TEXT,
    abstract TEXT,
    year INT,
    doi VARCHAR(255),
    domain VARCHAR(100)
);

-- Table authors
CREATE TABLE IF NOT EXISTS authors (
    author_id VARCHAR(50) PRIMARY KEY,
    author TEXT
);

CREATE TABLE keywords (
    keyword_id VARCHAR(50) PRIMARY KEY,
    keyword TEXT
);

CREATE TABLE article_author (
    id_article VARCHAR(50),
    author_id VARCHAR(50),
    PRIMARY KEY (id_article, author_id),
    FOREIGN KEY (id_article) REFERENCES articles(id_article),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

CREATE TABLE article_keyword (
    id_article VARCHAR(50),
    keyword_id VARCHAR(50),
    PRIMARY KEY (id_article, keyword_id),
    FOREIGN KEY (id_article) REFERENCES articles(id_article),
    FOREIGN KEY (keyword_id) REFERENCES keywords(keyword_id)
);

