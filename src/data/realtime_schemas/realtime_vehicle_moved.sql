DROP TABLE IF EXISTS realtime_vehicle_moved;

-- I wonder if a better tool for all this was a nosql database
CREATE TABLE realtime_vehicle_moved  (
  id SERIAL PRIMARY KEY,
  realtime_trip_id integer references realtime_trips(id),
  current_stop_sequence int,
  current_status varchar(20),
  observed_at integer
);


