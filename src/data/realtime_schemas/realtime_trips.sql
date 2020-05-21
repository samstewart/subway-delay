
DROP TABLE IF EXISTS realtime_trips;

CREATE TABLE realtime_trips (
  id VARCHAR(30) PRIMARY KEY,
  observed_at integer,
  start_date CHAR(10),
  route_id char(5) REFERENCES routes(id), 
  is_assigned boolean,
  direction CHAR(10),
  train_description VARCHAR(30) 
);

