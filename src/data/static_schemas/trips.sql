
DROP TABLE IF EXISTS trips;

CREATE TABLE trips (
  id char(10) not null primary key,
  route_id char(10) not null references routes(id),
  service_id char(100) not null references calendar(id),
  trip_headsign text,
  direction_id int,
  block_id text,
  shape_id text references shapes(id),
);


