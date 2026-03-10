create database traffic_analysis; /* creating the data base*/
select * from traffic_volume_log;
describe traffic_volume_log;
select count(*) from traffic_volume_log; /* 3000 records*/
select count(*) from signal_timing_config; /* 900 records*/
select count(*) from public_transport_delay_log; /* 3000 records*/

/* descriptive analysis on vehicle count*/
select 
count(vehicle_count_total) as n_records,
sum(vehicle_count_total) as total_vehicles,
min(vehicle_count_total) as min_count,
max(vehicle_count_total) as max_count,
avg(vehicle_count_total) as mean_count,
var_samp(vehicle_count_total) as variance_count,
stddev_samp(vehicle_count_total) as std_dev_count
from traffic_volume_log;

/* calculating median*/
/* total 3000 rcords ;; median = value at position 1500 and 1501 devided by 2*/
/* value at 1500*/
select vehicle_count_total from traffic_volume_log order by vehicle_count_total limit 1 offset 1499 ; -- 9
/* value at 1501 */
select vehicle_count_total from traffic_volume_log order by vehicle_count_total limit 1 offset 1500; -- 9
/* median = 9 */

/* calculating mode*/
SELECT vehicle_count_total, COUNT(*) AS freq
FROM traffic_volume_log
GROUP BY vehicle_count_total
ORDER BY freq DESC
LIMIT 1;

/* descriptive analyis for public transport delay data set*/
select
count(delay_minutes) as n_records,
sum(delay_minutes) as total_delay_minutes,
min(delay_minutes) as min_delay,
max(delay_minutes) as max_delay,
avg(delay_minutes) as mean_delay,
var_samp(delay_minutes) as variance_delay,
stddev_samp(delay_minutes) as stddev_delay
from public_transport_delay_log;

/* calculating median*/
/* total 3000 rcords ;; median = value at position 1500 and 1501 devided by 2*/
/* value at 1500*/
select delay_minutes from public_transport_delay_log order by delay_minutes limit 1 offset 1499 ; -- 5
/* value at 1501*/
select delay_minutes from public_transport_delay_log order by delay_minutes limit 1 offset 1500; -- 5
/* median = 5 */

/* calculation of mode*/
select delay_minutes,  count(*) as freq
from public_transport_delay_log
group by delay_minutes
order by freq desc
limit 1;

/* hourly pattern*/
select extract( hour from timestamp_utc) as hour , avg(vehicle_count_total) as avg_count 
from traffic_volume_log
group by hour order by hour;

/* daily traffic pattern */
select date as day, sum(vehicle_count_total) as total_vehicles 
from traffic_volume_log
group by date
order by day;

/* weekday vs weekend*/
SELECT 
CASE WHEN DAYOFWEEK(timestamp_utc) IN (1,7) THEN 'Weekend' ELSE 'Weekday' END AS day_type,
AVG(vehicle_count_total) AS avg_vehicle_count
FROM traffic_volume_log
GROUP BY day_type;

/* inersection based traffic*/
SELECT intersection_name, AVG(vehicle_count_total) AS avg_vehicles
FROM traffic_volume_log
GROUP BY intersection_name
ORDER BY avg_vehicles DESC
LIMIT 10;

/* delay reasons*/
select delay_reason, count(*) as freq
from public_transport_delay_log
group by delay_reason
order by freq desc;

/* route based delays*/
SELECT route_id, AVG(delay_minutes) AS avg_delay
FROM public_transport_delay_log
GROUP BY route_id
ORDER BY avg_delay DESC;

/* time of delay*/
SELECT EXTRACT(HOUR FROM scheduled_arrival_ts) AS hour, 
AVG(delay_minutes) AS avg_delay
FROM public_transport_delay_log
GROUP BY hour ORDER BY hour;


