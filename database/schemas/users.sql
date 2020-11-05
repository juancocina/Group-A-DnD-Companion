CREATE TABLE users (
        user_id text PRIMARY KEY, email text NOT NULL UNIQUE, 
        username text NOT NULL UNIQUE, password text NOT NULL);
