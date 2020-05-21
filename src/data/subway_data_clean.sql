/*
cql nyc_gtfs_development
onsider checking/running merge_trips.sql before running these queries
*/

-- chooses freshest estimated arrival / departure for each trip at each stop
-- one interesting question is to see how the estimates change over time? 
-- group by / distinct + sql ordering are equivalent?
CREATE TABLE estimated_stop_times AS
SELECT DISTINCT ON (realtime_trip_id, stop_mta_id) *
FROM stop_time_updates
ORDER BY realtime_trip_id, stop_mta_id, observed_at DESC;

SELECT DISTINCT ON (realtime_trip_id, stop_mta_id) realtime_trip_id, stop_mta_id, observed_at, co 
FROM stop_time_updates
ORDER BY realtime_trip_id, stop_mta_id, observed_at DESC;


-- how can we observe an arrival time in the past?
select realtime_trip_id, stop_mta_id, observed_at, coalesce(arrival_time, departure_time)
from test_estimated_stop_times 
--where realtime_trip_id = 849
order by realtime_trip_id, stop_mta_id, observed_at, departure_time;

-- I'm not sure I see why this is necessary given the above line?
-- things to do: 
-- 1. finish figuring out how to deal with fragment trips (can we find start and end of each trip?). so maybe need to understand the raw data better before we create the above tables. It appears we get a schedule for each trip every few seconds.
-- 2. find delays using vehicle_position and stop_time_updates
-- 3. recreate plot of several trips from his publication 
-- 4. exploratory question is to find for each line, which stops have the highest delays over a day (so delays by line, by stop)
DELETE FROM estimated_stop_times
WHERE COALESCE(arrival_time, departure_time) > observed_at + '5 minutes'::interval -- too far in future 
  OR COALESCE(arrival_time, departure_time) < observed_at - '20 minutes'::interval; -- too far in past ... does this even happen in the data? do we even have departure_time < observed_at?

CREATE INDEX ON estimated_stop_times (realtime_trip_id);
CREATE INDEX ON estimated_stop_times (stop_mta_id);

-- computation to get the start and end of each 
select realtime_trip_id, origin_name, row_number() over (partition by realtime_trip_id order by origin_departure) from time_between_stations ;

-- counting number of stops for L line 
select u.realtime_trip_id, count(*) from stop_time_updates u inner join realtime_trips t on t.id = u.realtime_trip_id and t.route_mta_id = 'L' group by u.realtime_trip_id;

-- my suspicion is that short trips because we cut off the recording process?
-- or because it doesn't give stop time updates for stations behind the current station?
-- could it be a transfer?
select t.id, t.first_observed_at, l.trip_length, t.route_mta_id, t.origin_location, t.destination_location from trip_lengths l inner join realtime_trips t on t.id = l.realtime_trip_id where l.trip_length < 6 order by t.route_mta_id;


-- very strange, the trip lengths are fairly uniformly distributed with the longest one being 24 stops. This is for the L line. Would like to know why?  is a good one to analyze.
select t.id, t.first_observed_at, l.trip_length, t.route_mta_id, t.origin_location, t.destination_location from estimated_trip_lengths l inner join realtime_trips t on t.id = l.realtime_trip_id where t.route_mta_id = 'L' order by l.trip_length desc;

-- the trip 849 is a L train that we have the arrival time for each stop 
select u.realtime_trip_id, u.stop_mta_id, s.name as stop_name, u.observed_at, coalesce(u.arrival_time, u.departure_time) as departure_time
from estimated_stop_times u
inner join stops s on s.mta_id = u.stop_mta_id
inner join realtime_trips t on t.id = u.realtime_trip_id
where t.route_mta_id = 'L' and t.id = 849
order by u.realtime_trip_id, stop_mta_id;

-- we want arrival and departure time so I can see how long we linger at the station
select u.realtime_trip_id, u.stop_mta_id, s.name as stop_name, u.observed_at, u.arrival_time, u.departure_time 
from estimated_stop_times u
inner join stops s on s.mta_id = u.stop_mta_id
inner join realtime_trips t on t.id = u.realtime_trip_id
where t.route_mta_id = 'L' and t.id = 849
order by u.realtime_trip_id, stop_mta_id;

select * from full_length_L_trips;


-- I think we want the 'observed_at' of the stop_time_updates and the 'observed_at' of the vehicle_position to determine if the train is stopped or not in realtime.
-- but we can find delays historically by looking at the transit_time_between stations. but what characterizes a delay? That's worth reading about...
-- What is the distribution on the transit times between stations?
-- Tomorrow's project is to estimate that from the data (just plot a histogram for each pairs of stops)

select observed_at, stop_mta_id from vehicle_positions where realtime_trip_id = 1230;

--ql nyc_gtfs_development
elect o.observed_at as observation_timestamp, u.departure_time as train_arrived_time, v.observed_at as train_moved_time from vehicle_positions v 
inner join realtime_feed_observations o
on o.id = v.observation_id
inner join stop_time_updates u
on u.observation_id = v.observation_id
and u.stop_mta_id in ('L17N', 'L15N')
and u.realtime_trip_id = 1230
where v.realtime_trip_id = 1230;

-- see the actual time we leave
select o.observed_at as observation_timestamp, v.observed_at as train_moved_time 
from vehicle_positions v 
inner join realtime_feed_observations o
on o.id = v.observation_id
where v.realtime_trip_id = 1230;

-- see the predicted time we're leaving
select u.stop_mta_id, u.observed_at, u.departure_time, u.arrival_time
from stop_time_updates u
where u.realtime_trip_id = 1230 and u.stop_mta_id in ('L15N', 'L17N')
order by u.stop_mta_id desc, u.observed_at;

-- the trip 847 has fewer delays

select * from stops;

select u.stop_mta_id, o.observed_at as observation_timestamp, u.departure_time, u.arrival_time, v.observed_at as train_moved_time from vehicle_positions v 
inner join realtime_feed_observations o
on o.id = v.observation_id
inner join stop_time_updates u
on u.observation_id = v.observation_id
where v.realtime_trip_id = 847 
and u.realtime_trip_id = 847
and u.stop_mta_id in ('L17N', 'L15N')
order by u.stop_mta_id desc, u.observed_at;


-- trying to understand train delays 
-- todo: the vehicleposition should inherit the observed_at tag
select u.stop_mta_id, o.observed_at as observation_timestamp, u.departure_time, u.arrival_time, v.observed_at as train_moved_time from vehicle_positions v 
inner join realtime_feed_observations o
on o.id = v.observation_id
inner join stop_time_updates u
on u.observation_id = v.observation_id
where v.realtime_trip_id = 1230 
and u.realtime_trip_id = 1230
and u.stop_mta_id in ('L17N', 'L15N')
order by u.stop_mta_id desc, u.observed_at;

-- somehow not everything is in the same timezone, which is really irritating. one is in nyc and the other is in utc.
select origin_departure + '5 hours'::interval, dest_arrival + '5 hours'::interval, transit_time from time_between_stations where route_mta_id = 'L' and realtime_trip_id = 1230 order by origin_departure;

create table full_length_L_trips as
select t.id, t.first_observed_at, l.trip_length, t.route_mta_id, t.origin_location, t.destination_location from estimated_trip_lengths l inner join realtime_trips t on t.id = l.realtime_trip_id where t.route_mta_id = 'L' and l.trip_length = 24 order by l.trip_length desc;

select t.id, t.first_observed_at, l.trip_length, t.route_mta_id, t.origin_location, t.destination_location from trip_lengths l inner join realtime_trips t on t.id = l.realtime_trip_id where t.route_mta_id = 'L' order by l.trip_length desc;

-- a trip on the L line that was cut off is 510, 513
select s.name, u.observed_at, u.arrival_time 
from stop_time_updates u
inner join stops s
on s.mta_id = u.stop_mta_id
where realtime_trip_id = 510;

create table estimated_trip_lengths as
select realtime_trip_id, count(*) as trip_length
from estimated_stop_times 
group by realtime_trip_id;


create table trip_lengths as
select realtime_trip_id, count(*) as trip_length
from stop_time_updates 
group by realtime_trip_id;

select * from trip_lengths where trip_length < 5;

select u.realtime_trip_id, u.stop_mta_id, u.observed_at, u.departure_time from stop_time_updates u inner join realtime_trips t on t.id = u.realtime_trip_id and u.realtime_trip_id = 510;

select t.first_observed_at, t.most_recently_observed_at from L_train_lengths l inner join realtime_trips t on t.id = l.realtime_trip_id and l.count < 10;

-- length of realtime trips in number of stops
CREATE TABLE realtime_trip_lengths AS 
select 
	realtime_trip_id, count(*) as trip_length
from time_between_stations 
group by realtime_trip_id;

CREATE TEMP TABLE tmp_realtime_trips AS
SELECT
  id,
  direction,
  CASE route_mta_id WHEN '5X' THEN '5' ELSE route_mta_id END AS route_mta_id
FROM realtime_trips;
CREATE UNIQUE INDEX ON tmp_realtime_trips (id);

-- combines stop_time_updates and realtime_trips (a realtime_trip has many stop_time_updates -- one for each stop)
-- the stop_time_updates contains the actual departure info and the realtime_trip is just meta-data about the whole trip (direction and stops, etc.)
-- how does his code choose the most recent updates for time between trains?
CREATE TABLE times_between_trains AS
SELECT
  u.stop_mta_id,
  s.name AS stop_name,
  t.route_mta_id,
  t.direction,
  COALESCE(u.departure_time, u.arrival_time) AT TIME ZONE 'UTC' AT TIME ZONE 'America/New_York' AS departure_time,
-- find the next departure by looking at all scheduled departures at the same stop, along the same route, and in the same direction. Then find the next one in line. 
-- coalesce just takes the non-null of the two (departure and arrival time are the same for this analysis)
  EXTRACT(
    EPOCH FROM
    LEAD(COALESCE(u.departure_time, u.arrival_time), 1) OVER w - COALESCE(u.departure_time, u.arrival_time)
  ) AS seconds_until_next_departure,
  u.realtime_trip_id,
  LEAD(u.realtime_trip_id, 1) OVER w AS next_realtime_trip_id
FROM estimated_stop_times u
  INNER JOIN tmp_realtime_trips t ON u.realtime_trip_id = t.id
  INNER JOIN stops s ON u.stop_mta_id = s.mta_id
WINDOW w AS (
  PARTITION BY u.stop_mta_id, t.route_mta_id, t.direction
  ORDER BY COALESCE(u.arrival_time, u.departure_time)
)
ORDER BY u.stop_mta_id, t.route_mta_id, t.direction, COALESCE(u.arrival_time, u.departure_time);

-- remove probable data errors. less than 0.2% of rows
DELETE FROM times_between_trains WHERE seconds_until_next_departure < 20;

-- remove likely scheduled maintenance windows
DELETE FROM times_between_trains WHERE seconds_until_next_departure > 60 * 60 * 2;

CREATE INDEX ON times_between_trains (stop_mta_id);
CREATE INDEX ON times_between_trains (route_mta_id);

CREATE TABLE route_stop_direction_counts AS
SELECT route_mta_id, stop_mta_id, direction, COUNT(*)
FROM times_between_trains
GROUP BY route_mta_id, stop_mta_id, direction;

CREATE TABLE subway_data_clean AS
SELECT
  t.realtime_trip_id,
  t.stop_mta_id,
  t.route_mta_id,
  t.direction,
  t.departure_time,
  t.seconds_until_next_departure
FROM times_between_trains t
  INNER JOIN route_stop_direction_counts c
    ON t.stop_mta_id = c.stop_mta_id
    AND t.route_mta_id = c.route_mta_id
    AND t.direction = c.direction
WHERE seconds_until_next_departure BETWEEN 20 AND (60 * 60 * 2)
  AND (
    c.count > 1000
    OR (c.route_mta_id = 'Z' AND c.count > 300)
  );

-- much cleaner construction than our construction using LEAD
CREATE TABLE station_to_station_travel_times AS
SELECT
  t1.realtime_trip_id,
  rt.route_mta_id,
  t1.stop_mta_id AS from_stop_mta_id,
  t2.stop_mta_id AS to_stop_mta_id,
  t1.departure_time,
  t2.arrival_time,
  EXTRACT(EPOCH FROM t2.arrival_time - t1.departure_time) AS duration
FROM estimated_stop_times t1
  INNER JOIN estimated_stop_times t2
    ON t1.realtime_trip_id = t2.realtime_trip_id
    AND t2.arrival_time > t1.departure_time
  INNER JOIN realtime_trips rt
    ON t1.realtime_trip_id = rt.id
WHERE t2.arrival_time IS NOT NULL
  AND t1.departure_time IS NOT NULL
ORDER BY t1.realtime_trip_id, t1.departure_time, t2.arrival_time;


--- get list of predictions of train trajectory through time (only contains projections for stops with departures ahead of us

select observed_at, departure_time, s.name from stop_time_updates u inner join stops s on s.mta_id = u.stop_mta_id where realtime_trip_id = 849 order by observed_at, departure_time;

CREATE TABLE station_to_station_summary AS
SELECT
  route_mta_id,
  from_stop_mta_id,
  to_stop_mta_id,
  COUNT(*) AS trips,
  percentile_cont(0.1) WITHIN GROUP (ORDER BY duration) AS pct10,
  percentile_cont(0.25) WITHIN GROUP (ORDER BY duration) AS pct25,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY duration) AS pct50,
  percentile_cont(0.75) WITHIN GROUP (ORDER BY duration) AS pct75,
  percentile_cont(0.9) WITHIN GROUP (ORDER BY duration) AS pct90,
  AVG(duration) AS mean
FROM station_to_station_travel_times
WHERE EXTRACT(dow FROM departure_time) BETWEEN 1 AND 5
  AND EXTRACT(hour FROM departure_time) BETWEEN 7 AND 19
  AND duration BETWEEN 15 AND (6 * 60 * 60)
GROUP BY route_mta_id, from_stop_mta_id, to_stop_mta_id
ORDER BY from_stop_mta_id, to_stop_mta_id, route_mta_id;

CREATE TABLE station_to_station_summary_yearly AS
SELECT
  route_mta_id,
  from_stop_mta_id,
  to_stop_mta_id,
  EXTRACT(year FROM departure_time) AS year,
  COUNT(*) AS trips,
  percentile_cont(0.1) WITHIN GROUP (ORDER BY duration) AS pct10,
  percentile_cont(0.25) WITHIN GROUP (ORDER BY duration) AS pct25,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY duration) AS pct50,
  percentile_cont(0.75) WITHIN GROUP (ORDER BY duration) AS pct75,
  percentile_cont(0.9) WITHIN GROUP (ORDER BY duration) AS pct90,
  AVG(duration) AS mean
FROM station_to_station_travel_times
WHERE EXTRACT(dow FROM departure_time) BETWEEN 1 AND 5
  AND EXTRACT(hour FROM departure_time) BETWEEN 7 AND 19
  AND duration BETWEEN 15 AND (6 * 60 * 60)
GROUP BY route_mta_id, from_stop_mta_id, to_stop_mta_id, year
ORDER BY from_stop_mta_id, to_stop_mta_id, route_mta_id, year;
