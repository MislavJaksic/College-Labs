select * from crosstab('select query,
			date_trunc(''hour'', date_and_time) as times,
			count(*)
			from queries
			where date_and_time >= ''1999-01-9'' and
			      date_and_time <= ''1999-01-12''
			group by query, times
			order by query, times;',
			'select d from generate_series(''1999-01-9''::timestamp, ''1999-01-12'', ''1 hour'') d;')
as ct(query character varying(255), day_hour_one bigint); --need 74 bigint columns