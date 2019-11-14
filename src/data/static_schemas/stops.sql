
DROP TABLE IF EXISTS stops;

CREATE TABLE stops (
  id char(10) primary key,
  stop_code text default null,
  stop_name text default null,
  stop_desc text default null,
  stop_lat double precision,
  stop_lon double precision,
  zone_id text,
  stop_url text,
  location_type integer default null,
  parent_station text default null
);


