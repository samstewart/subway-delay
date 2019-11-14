
DROP TABLE IF EXISTS realtime_trips;

CREATE TABLE realtime_trips (
  id SERIAL PRIMARY KEY,
  observed_at integer,
  start_date integer,
  route_id char(5) REFERENCES routes(id), 
  is_assigned boolean,
  direction CHAR(1)
  train_description VARCHAR(30) 
);


