select query,
       extract(day from date_and_time) as days,
       count(*)
from queries
where date_and_time >= '1999-01-07' and
      date_and_time <= '1999-01-12'
group by query, days
order by query, days;