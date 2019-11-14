
DROP TABLE IF EXISTS routes;

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


