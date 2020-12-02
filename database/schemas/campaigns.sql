PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS "campaigns"
(
    campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id int,
    date_created TEXT,
    campaign_name TEXT,
    campaign_description TEXT,
    thumbnail_path TEXT
);
CREATE TABLE IF NOT EXISTS "maps"
(
    map_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id int,
    user_id int,
    map_name TEXT,
    map_description TEXT,
    map_path TEXT,
    FOREIGN KEY(campaign_id) REFERENCES campaigns(campaign_id),
    FOREIGN KEY(user_id) REFERENCES campaigns(user_id)
);