CREATE TABLE IF NOT EXISTS recipe_ingredient (
           id SERIAL PRIMARY KEY,
           recipe_id INTEGER,
           ingredient_id INTEGER,
           info TEXT,
           amount TEXT,
           FOREIGN KEY (recipe_id) REFERENCES recipes(id),
           FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
       );
