## Задача проекта
Цель проекта - проаналищировать рейсы из Анапы в зимниемесяцы 2017 года и отобрать убыточные или малоприбыльные полёты.
***
## Коротко о данных
В наборе данных присутствует 127 строк, 26 столбцов, 15 из которых используются в анализе, остальные являются вмпоиогательными из которых выведены другие столбцы.
***
## Запросы к вопросам и выбору основных данных
### Задание 4.1
```SQL
SELECT city,
       count(airport_code) AS airports
FROM dst_project.airports
GROUP BY city
HAVING count(airport_code) > 1
```

### Задание 4.2
#### Вопрос 1
``` sql
SELECT count(DISTINCT status) AS statuses
FROM dst_project.flights
```

#### Вопрос 2
``` sql
SELECT COUNT(*) AS flights_count
FROM dst_project.flights
WHERE status = 'Departed'
```

#### Вопрос 3
``` sql
SELECT count(st.seat_no) AS seats
FROM dst_project.seats st
WHERE st.aircraft_code = '773'
```

#### Вопрос 4
``` sql
SELECT count(*)
FROM dst_project.flights fl
WHERE fl.actual_arrival BETWEEN '2017-04-01' AND '2017-08-31'
  AND fl.status = 'Arrived'
```

### Задание 4.3
#### Вопрос 1
``` sql
SELECT count(*)
FROM dst_project.flights fl
WHERE fl.status = 'Cancelled'
```

#### Вопрос 2
``` sql
SELECT 'Boeing' AS manufacturer,
       count(aircraft_code) AS aircrafts
FROM dst_project.aircrafts a
WHERE model like 'Boeing%'
UNION ALL
SELECT 'Airbus' AS manufacturer,
       count(aircraft_code) AS aircrafts
FROM dst_project.aircrafts a
WHERE model like 'Airbus%'
UNION ALL
SELECT 'Sukhoi Superjet' AS manufacturer,
       count(aircraft_code) AS aircrafts
FROM dst_project.aircrafts a
WHERE model like 'Sukhoi Superjet%'
```

#### Вопрос 3
``` sql
SELECT substr(timezone, 1, strpos(timezone, '/')-1) AS continent,
       count(airport_code) AS airports
FROM dst_project.airports a
GROUP BY continent
```

#### Вопрос 4
``` sql
SELECT fl.*,
       (actual_arrival - scheduled_arrival) AS diff
FROM dst_project.flights fl
WHERE actual_arrival IS NOT NULL
ORDER BY diff DESC
LIMIT 1
```

### Задание 4.4
#### Вопрос 1
``` sql
	select min(scheduled_departure) as first_flight from dst_project.flights fl
```

#### Вопрос 2
``` sql
select extract(epoch from (fl.scheduled_arrival - fl.scheduled_departure)::interval)/60 as flight_time from dst_project.flights fl
order by fl.scheduled_arrival - fl.scheduled_departure desc 
limit 1
```


#### Вопрос 3
``` sql
select fl.*, (fl.scheduled_arrival - fl.scheduled_departure) as scheduled_flight_time from dst_project.flights fl 
where departure_airport = 'DME' and arrival_airport in ('UUS','AAQ','PCS') or departure_airport = 'SVO' and arrival_airport = 'UUS'
order by (fl.scheduled_arrival - fl.scheduled_departure) desc 
limit 1
```

#### Вопрос 4
``` sql
select avg(extract(epoch from (fl.scheduled_arrival - fl.scheduled_departure)::interval)/60) as avg_flight_time from dst_project.flights fl
```

### Задание 4.5
#### Вопрос 1
``` sql
	select fare_conditions, count(seat_no) as seats from dst_project.seats s
where s.aircraft_code = 'SU9'
group by fare_conditions
order by count(seat_no) desc limit 1
```

#### Вопрос 2
``` sql
select min(total_amount) as min_amount from dst_project.bookings
```

#### Вопрос 3
``` sql
select * from dst_project.tickets t
inner join dst_project.boarding_passes bp on bp.ticket_no = t.ticket_no
where passenger_id = '4313 788533' 
```

### Данные для анализа
#### Данные по направлениям

``` sql
SELECT arrival_airport,
       city,
       sum(flight_profit) AS profit,
       count(CASE
                 WHEN flight_profit > 0 THEN flight_profit
                 ELSE NULL
             END) AS profit_flights,
       count(CASE
                 WHEN flight_profit < 0 THEN flight_profit
                 ELSE NULL
             END) AS non_profit_flights,
       avg(flight_profit) AS average_profit
FROM
  (SELECT init_data.*,
          fuel_consumption_rate * flight_time_hours AS fuel_burned,
          fuel_consumption_rate * flight_time_hours * fuel_price_for_ton AS fuel_cost,
          ticket_income - fuel_consumption_rate * flight_time_hours * fuel_price_for_ton AS flight_profit
   FROM
     (SELECT fl.*,
             ap.city,
             ac.model,
             fl.actual_departure - fl.scheduled_departure AS departure_delay,
             fl.actual_arrival - fl.scheduled_arrival AS arrival_delay,
             sum(coalesce(tf.amount, 0)) AS ticket_income,
             fl.scheduled_arrival - fl.scheduled_departure AS scheduled_flight_time,
             fl.actual_arrival - fl.actual_departure AS actual_flight_time,
             (fl.scheduled_arrival - fl.scheduled_departure) - (fl.actual_arrival - fl.actual_departure) AS flight_time_diff,
             (CASE
                  WHEN fl.aircraft_code = '733' THEN 2.400
                  ELSE CASE
                           WHEN fl.aircraft_code = 'SU9' THEN 1.700
                           ELSE 1
                       END
              END) AS fuel_consumption_rate,
             extract(epoch
                     FROM (fl.actual_arrival - fl.actual_departure)::interval)/3600 AS flight_time_hours,
             CASE
                 WHEN scheduled_departure BETWEEN '2017-01-01' AND '2017-02-01' THEN 41435
                 ELSE CASE
                          WHEN scheduled_departure BETWEEN '2017-02-01' AND '2017-03-01' THEN 39553
                          ELSE CASE
                                   WHEN scheduled_departure BETWEEN '2017-12-01' AND '2018-01-01' THEN 47101
                                   ELSE 0
                               END
                      END
             END AS fuel_price_for_ton
      FROM dst_project.flights fl
      LEFT JOIN dst_project.ticket_flights tf ON tf.flight_id = fl.flight_id
      INNER JOIN dst_project.aircrafts ac ON ac.aircraft_code = fl.aircraft_code
      INNER JOIN dst_project.airports ap ON ap.airport_code = fl.arrival_airport
      WHERE departure_airport = 'AAQ'
        AND (date_trunc('month', scheduled_departure) in ('2017-01-01',
                                                          '2017-02-01',
                                                          '2017-12-01'))
        AND status not in ('Cancelled')
      GROUP BY fl.flight_id,
               ap.city,
               ac.model) AS init_data) AS profits
GROUP BY arrival_airport,
         city
ORDER BY profit
```

#### Прибыльные рейсы
``` sql
WITH profits AS
  (SELECT init_data.*,
          fuel_consumption_rate * flight_time_hours AS fuel_burned,
          fuel_consumption_rate * flight_time_hours * fuel_price_for_ton AS fuel_cost,
          ticket_income - fuel_consumption_rate * flight_time_hours * fuel_price_for_ton AS flight_profit
   FROM
     (SELECT fl.*,
             ap.city,
             ac.model,
             fl.actual_departure - fl.scheduled_departure AS departure_delay,
             fl.actual_arrival - fl.scheduled_arrival AS arrival_delay,
             SUM(COALESCE(tf.amount, 0)) AS ticket_income,
             fl.scheduled_arrival - fl.scheduled_departure AS scheduled_flight_time,
             fl.actual_arrival - fl.actual_departure AS actual_flight_time,
             (fl.scheduled_arrival - fl.scheduled_departure) - (fl.actual_arrival - fl.actual_departure) AS flight_time_diff,
             (CASE
                  WHEN fl.aircraft_code = '733' THEN 2.400
                  ELSE CASE
                           WHEN fl.aircraft_code = 'SU9' THEN 1.700
                           ELSE 1
                       END
              END) AS fuel_consumption_rate,
             EXTRACT(epoch
                     FROM (fl.actual_arrival - fl.actual_departure):: INTERVAL)/3600 AS flight_time_hours,
             CASE
                 WHEN scheduled_departure BETWEEN '2017-01-01' AND '2017-02-01' THEN 41435
                 ELSE CASE
                          WHEN scheduled_departure BETWEEN '2017-02-01' AND '2017-03-01' THEN 39553
                          ELSE CASE
                                   WHEN scheduled_departure BETWEEN '2017-12-01' AND '2018-01-01' THEN 47101
                                   ELSE 0
                               END
                      END
             END AS fuel_price_for_ton
      FROM dst_project.flights fl
      LEFT JOIN dst_project.ticket_flights tf ON tf.flight_id = fl.flight_id
      INNER JOIN dst_project.aircrafts ac ON ac.aircraft_code = fl.aircraft_code
      INNER JOIN dst_project.airports ap ON ap.airport_code = fl.arrival_airport
      WHERE departure_airport = 'AAQ'
        AND (date_trunc('month', scheduled_departure) in ('2017-01-01',
                                                          '2017-02-01',
                                                          '2017-12-01'))
        AND STATUS NOT in ('Cancelled')
      GROUP BY fl.flight_id,
               ap.city,
               ac.model) AS init_data),
     profits_averages AS
  (SELECT profits.arrival_airport,
          round(AVG(profits.flight_profit::decimal), 2) AS average_airport_profit
   FROM profits
   GROUP BY profits.arrival_airport),
     average AS
  (SELECT round(AVG(profits.flight_profit::decimal), 2) AS flights_average
   FROM profits)
SELECT profits.*,
       ROUND(profits.flight_profit::decimal - pa.average_airport_profit::decimal, 2) AS diff_arrival_airport,
       ROUND(profits.flight_profit::decimal - average.flights_average::decimal, 2) AS diff_flights_average
FROM profits
INNER JOIN profits_averages pa ON pa.arrival_airport = profits.arrival_airport
CROSS JOIN average
WHERE profits.flight_profit > 0
ORDER BY diff_flights_average
```		 