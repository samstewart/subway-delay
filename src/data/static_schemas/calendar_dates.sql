DROP TABLE IF EXISTS calendar_dates;


CREATE TABLE calendar_dates (
  service_id text,
  date date not null,
  exception_type int 
);

CREATE INDEX ON calendar_dates (date);


