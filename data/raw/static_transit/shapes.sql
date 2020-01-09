
DROP TABLE IF EXISTS shapes CASCADE;

CREATE TABLE shapes (
  id text,
  shape_pt_lat double precision not null,
  shape_pt_lon double precision not null,
  shape_pt_sequence int not null,
  shape_dist_traveled double precision default null
);

CREATE INDEX id_idx ON shapes(id);
