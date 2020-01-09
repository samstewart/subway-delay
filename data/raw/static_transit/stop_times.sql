
DROP TABLE IF EXISTS stop_times;

CREATE TABLE stop_times (
  trip_id text references trips(id),
  -- unfortunately, we can't use 'time' data type because there is an error in the source data. They have 24:02:00. I can clean that, but I don't need these times so I'll just enter them as character strings. 
  arrival_time char(10), 
  departure_time char(10), 
  stop_id text references stops(id),
  stop_sequence int not null,
  stop_headsign text,
  pickup_type int,
  drop_off_type int ,
  shape_dist_traveled numeric(10, 2),
  PRIMARY KEY (trip_id, stop_id)
);

-- if we set something as the primary key, doesn't that automatically create an index?
--CREATE INDEX ON stop_times (trip_id, stop_id);


