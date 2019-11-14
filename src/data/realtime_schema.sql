DROP TABLE IF EXISTS stop_time_update;
DROP TABLE IF EXISTS trip;
DROP TABLE IF EXISTS alert;

CREATE TABLE stop_time_update (
  id SERIAL PRIMARY KEY,
  stop_id varchar(10) references routes(id), -- comes from 'stops' table with static data
  arrival interval,
  departure interval,
  observed_at interval,
  schedule_relationship VARCHAR(20),
  scheduled_track integer,
  actual_track integer 
);

CREATE TABLE realtime_trips (
  id SERIAL PRIMARY KEY,
  observed_at interval,
  start_date interval,
  route_id char(5) REFERENCES routes(id), -- needs to be obtained from routes table
  is_assigned boolean,
  direction CHAR(1)
  train_description VARCHAR(30) 
);

-- I wonder if a better tool for all this was a nosql database
CREATE TABLE vehicle (
  id SERIAL PRIMARY KEY,
  realtime_trip_id integer references realtime_trips(id),
  current_stop_sequence int,
  current_status varchar(20),
  observed_at interval
);

CREATE TABLE vehicle (
  id SERIAL PRIMARY KEY,
  realtime_trip_id integer references realtime_trips(id),
  current_stop_sequence int,
  current_status varchar(20),
  observed_at interval
);


