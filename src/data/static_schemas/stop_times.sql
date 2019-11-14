
DROP TABLE IF EXISTS stop_times;
CREATE TABLE stop_times (
  trip_id text references trips(id),
  -- Check that casting to time integer works.
  arrival_time integer, 
  departure_time integer, 
  stop_id text references stops(id),
  stop_sequence int not null,
  stop_headsign text,
  pickup_type int,
  drop_off_type int ,
  shape_dist_traveled numeric(10, 2),
  PRIMARY KEY (trip_id, stop_sequence)
);

CREATE INDEX ON stop_times (trip_id, stop_id);


