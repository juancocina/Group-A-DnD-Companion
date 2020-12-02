CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, email text NOT NULL UNIQUE, 
        username text NOT NULL UNIQUE, hashed_password text NOT NULL);
