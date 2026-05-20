-- users
CREATE TABLE IF NOT EXISTS users(
    chat_id INTEGER PRIMARY KEY,
    username TEXT DEFAULT 'user',
    languge TEXT DEFAULT 'en'
);

-- assets
CREATE TABLE IF NOT EXISTS assets(
    coin_name TEXT PRIMARY KEY
);

-- subscribers
CREATE TABLE IF NOT EXISTS subscribers(
    chat_id INTEGER,
    coin TEXT,
    percent REAL DEFAULT 0.1,
    last_price REAL DEFAULT 0,
    PRIMARY KEY(chat_id, coin),
    FOREIGN KEY(coin) REFERENCES assets(coin_name),
    FOREIGN KEY(chat_id) REFERENCES users(chat_id)
);