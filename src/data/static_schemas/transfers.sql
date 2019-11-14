DROP TABLE IF EXISTS transfers;


CREATE TABLE transfers (
  from_stop_id text references stops(id),
  to_stop_id text references stops(id),
  transfer_type int,
  min_transfer_time int
);

