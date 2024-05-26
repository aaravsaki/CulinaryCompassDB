DROP TABLE IF EXISTS person_fooditem;
DROP TABLE IF EXISTS meal_has;
DROP TABLE IF EXISTS meal;
DROP TABLE IF EXISTS fooditem;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS email;

CREATE TABLE person(
  user_id integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  username text UNIQUE
);

CREATE TABLE email(
  mail text PRIMARY KEY,
  delivery_prob integer
);

CREATE TABLE meal(
  meal_id integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  name text,
  user_id integer,
  date timestamp,
  FOREIGN KEY (user_id) REFERENCES person(user_id) ON DELETE CASCADE
);

CREATE TABLE fooditem(
  item_id integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  name text, 
  calories integer,
  protein integer,
  fat integer,
  carbs integer,
  fiber integer,
  sodium integer,
  cholesterol integer,
  vitamin_a integer,
  vitamin_b integer,
  vitamin_c integer,
  vitamin_d integer,
  vitamin_e integer,
  vitamin_k integer,
  zinc integer,
  potassium integer,
  magnesium integer,
  calcium integer,
  iron integer,
  selenium integer
);

CREATE TABLE meal_has(
  meal_id integer,
  food_id integer,
  amount integer DEFAULT 1,
  FOREIGN KEY (meal_id) REFERENCES meal(meal_id) ON DELETE CASCADE,
  FOREIGN KEY (food_id) REFERENCES fooditem(item_id) ON DELETE CASCADE,
  PRIMARY KEY (meal_id, food_id)
);

CREATE TABLE person_fooditem(
  food_id integer,
  user_id integer,
  FOREIGN KEY (food_id) REFERENCES fooditem(item_id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES person(user_id) ON DELETE CASCADE,
  PRIMARY KEY (food_id, user_id)
)

CREATE OR REPLACE FUNCTION get_month_schedule(user_name text, month integer)
RETURNS table(mealname text, date timestamp, fooditems text[]) AS
$$
  SELECT m.name, m.date, array_agg(f.name) fooditems FROM meal m
    INNER JOIN meal_has mh ON mh.meal_id = m.meal_id
    INNER JOIN fooditem f ON f.item_id = mh.food_id
  WHERE EXTRACT(MONTH FROM m.date) = month
  GROUP BY m.user_id, m.name, m.date
  HAVING m.user_id = (SELECT user_id FROM person p WHERE p.username = user_name)
$$ language sql;

CREATE OR REPLACE FUNCTION get_day_schedule(user_name text, day text)
RETURNS table(mealname text, date timestamp, fooditems text[]) AS
$$
  SELECT m.name, m.date, array_agg(f.name) fooditems FROM meal m
    LEFT OUTER JOIN meal_has mh ON mh.meal_id = m.meal_id
    LEFT OUTER JOIN fooditem f ON f.item_id = mh.food_id
  WHERE DATE(m.date) = TO_DATE(day, 'YYYY-MM-DD')
  GROUP BY m.user_id, m.name, m.date
  HAVING m.user_id = (SELECT user_id FROM person p WHERE p.username = user_name)
$$ language sql;

CREATE OR REPLACE FUNCTION get_nutrition_info(user_name text, food_item text)
RETURNS json as
$$
  SELECT json_agg(f) FROM fooditem f
    INNER JOIN person_fooditem pf ON pf.food_id = f.item_id
    WHERE f.name = food_item
    GROUP BY pf.user_id, f.name
    HAVING pf.user_id = (SELECT user_id FROM person p WHERE p.username = user_name)
$$ language sql;

CREATE OR REPLACE FUNCTION get_item_ids(user_name text, food_name text)
RETURNS table(item_id integer) AS
$$
  SELECT item_id FROM fooditem f
    INNER JOIN person_fooditem pf ON f.item_id = pf.food_id
  WHERE f.name LIKE food_name AND pf.user_id = (SELECT user_id FROM person WHERE username = user_name)
$$ language sql;

