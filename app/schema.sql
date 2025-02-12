DROP TABLE IF EXISTS games;

CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT NOT NULL UNIQUE,
    createdAt TEXT,
    updatedAt TEXT,
    name TEXT,
    difficulty TEXT,
    gameState TEXT,
    board TEXT
);
