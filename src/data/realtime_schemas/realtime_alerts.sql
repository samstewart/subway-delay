DROP TABLE IF EXISTS realtime_alert;

CREATE TABLE realtime_alerts  (
  id SERIAL PRIMARY KEY,
  realtime_trip_id integer references realtime_trips(id),
-- might be any one of the following:
-- 1. a delay of a whole trip
-- 2. a problem at a stop
-- 3. a problem on a route 
-- In practice, I'm not sure what we'll see from nyc subway
  route_id char(5) references routes(id), -- can be null
  realtime_trip_id char(5) references realtime_trips(id), -- can be null
  current_stop_sequence int,
  current_status varchar(20),
  description text,
  observed_at integer -- unix timestamp
);

