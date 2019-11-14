-- stolen and reduced from https://github.com/BlinkTagInc/gtfs-to-mysql/blob/master/gtfs_to_mysql.sql

DROP TABLE IF EXISTS stops;
DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS calendar;
DROP TABLE IF EXISTS calendar_dates;
DROP TABLE IF EXISTS shapes;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS stop_times;
DROP TABLE IF EXISTS transfers;

CREATE TABLE calendar (
  id char(100) PRIMARY KEY,
  monday int not null,
  tuesday int not null,
  wednesday int not null,
  thursday int not null,
  friday int not null,
  saturday int not null,
  sunday int not null,
  start_date date not null,
  end_date date not null
);

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

CREATE TABLE routes (
  id char(5) primary key,
  agency_id text,
  route_short_name text default '',
  route_long_name text default '',
  route_desc text default '',
  route_type int,
  route_url text,
  route_color text,
  route_text_color text,
  dummy_column text
);

CREATE TABLE calendar_dates (
  service_id text,
  date date not null,
  exception_type int 
);

CREATE INDEX ON calendar_dates (date);

CREATE TABLE shapes (
  id text primary key,
  shape_pt_lat double precision not null,
  shape_pt_lon double precision not null,
  shape_pt_sequence int not null,
  shape_dist_traveled double precision default null
);

CREATE TABLE trips (
  id char(10) not null primary key,
  route_id char(10) not null references routes(id),
  service_id char(100) not null references calendar(id),
  trip_headsign text,
  direction_id int,
  block_id text,
  shape_id text references shapes(id),
);

CREATE TABLE stop_times (
  trip_id text references trips(id),
  -- Check that casting to time interval works.
  arrival_time interval, 
  departure_time interval, 
  stop_id text references stops(id),
  stop_sequence int not null,
  stop_headsign text,
  pickup_type int,
  drop_off_type int ,
  shape_dist_traveled numeric(10, 2),
  PRIMARY KEY (trip_id, stop_sequence)
);

CREATE INDEX ON stop_times (trip_id, stop_id);

CREATE TABLE transfers (
  from_stop_id text references stops(id),
  to_stop_id text references stops(id),
  transfer_type int,
  min_transfer_time int
);

