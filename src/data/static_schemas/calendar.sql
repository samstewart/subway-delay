
DROP TABLE IF EXISTS calendar;

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

