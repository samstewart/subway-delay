
DROP TABLE IF EXISTS trips CASCADE;

CREATE TABLE trips (
  route_id char(10) references routes(id),
  service_id char(100) not null references calendar(id),
  id char(100) primary key,
  trip_headsign text,
  direction_id int,
  block_id text,
  shape_id text
);


