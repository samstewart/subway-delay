
DROP TABLE IF EXISTS realtime_stop_time_update;

CREATE TABLE realtime_stop_time_update (
  id SERIAL PRIMARY KEY,
  realtime_trip_id v
  stop_id varchar(10) references routes(id), 
  arrival integer,
  departure integer,
  observed_at integer,
  schedule_relationship VARCHAR(20),
  scheduled_track integer,
  actual_track integer 
);


