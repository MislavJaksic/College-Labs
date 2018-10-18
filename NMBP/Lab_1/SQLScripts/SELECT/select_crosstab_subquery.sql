select query,
       date_trunc('day', date_and_time) as times,
       count(*)
from queries
where date_and_time >= '1999-01-9' and
      date_and_time <= '1999-01-12'
group by query, times
order by query, times;