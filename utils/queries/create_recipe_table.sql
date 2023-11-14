CREATE TABLE IF NOT EXISTS recipes (
           id SERIAL PRIMARY KEY,
           title TEXT,
           url TEXT,
           preparation_time TEXT,
           calories TEXT,
           description TEXT,
           portions TEXT,
           image BYTEA,
           category TEXT
       );