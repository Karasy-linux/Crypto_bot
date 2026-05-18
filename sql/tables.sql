-- users
CREATE TABLE IF NOT EXISTS users(
    chat_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL
);


-- assets
CREATE TABLE IF NOT EXISTS assets(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);   


--subscribers
CREATE TABLE IF NOT EXISTS subscribers(
    chat_id INTEGER,
    asset_id INTEGER,
    percent REAL DEFAULT 0.1,
    last_price REAL,
    PRIMARY KEY(chat_id, asset_id),
    FOREIGN KEY (chat_id) REFERENCES users(chat_id),
    FOREIGN KEY (asset_id) REFERENCES assets(id)

);


-- histoty
-- CREATE TABLE IF NOT EXISTS history(
--    id INTEGER PRIMARY KEY AUTOINCREMENT,
--    price REAL,
--    asset_id INTEGER,
--    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
--    FOREIGN KEY (asset_id) REFERENCES assets(id)
--); 
