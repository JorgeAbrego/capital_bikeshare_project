WITH preprocessed_rides AS (
    SELECT
        ride_id,
        rideable_type,
        started_at,
        ended_at,
        start_station_name,
        start_station_id,
        end_station_name,
        end_station_id,
        start_lat,
        start_lng,
        end_lat,
        end_lng,
        member_casual,
        DATE(started_at) as started_at_date,
        EXTRACT(DAYOFWEEK FROM started_at) as day_of_week,
        FORMAT_DATE('%A', DATE(started_at)) as day_name,
        EXTRACT(HOUR FROM started_at) as start_hour,
        TIMESTAMP_DIFF(ended_at, started_at, MINUTE) as duration_minutes,
        CASE 
            WHEN EXTRACT(HOUR FROM started_at) BETWEEN 0 AND 6 THEN 'Night'
            WHEN EXTRACT(HOUR FROM started_at) BETWEEN 7 AND 12 THEN 'Morning'
            WHEN EXTRACT(HOUR FROM started_at) BETWEEN 13 AND 18 THEN 'Afternoon'
            ELSE 'Evening'
        END as time_of_day
    FROM
        {{ source('staging','prt_bikeshare') }}
)

SELECT
    *,
    CASE
        WHEN duration_minutes <= 30 THEN 'Short'
        WHEN duration_minutes BETWEEN 31 AND 60 THEN 'Medium'
        ELSE 'Long'
    END as ride_length_category
FROM
    preprocessed_rides
