do $$
DECLARE
	row record;
	ballot int;
	current_user_id uuid;
	random_date_time timestamp;
	temp_id int;
	temp_user_id uuid;
	temp_int int;
BEGIN
	for row in (select * from users) LOOP
		current_user_id := row.id;
		-- Generate infection history
		-- SELECT floor(random()*(b-a+1))+a;
		ballot := (select floor(random()*(5-0+1))+0);
		for i in 1..ballot LOOP
			random_date_time := (
				select timestamp '2020-01-01 00:00:00' +
			   random() * (timestamp '2022-09-11 12:00:00' -
						   timestamp '2020-01-01 00:00:00')
								);
			insert into infectionhistory(user_id, recorded_timestamp) values(current_user_id, random_date_time);
		END LOOP;
		-- Generate vaccinationhistory
		ballot := (select floor(random()*(5-0+1))+0);
		for i in 1..ballot LOOP
			random_date_time := (
				select date(timestamp '2020-01-01 00:00:00' +
			   random() * (timestamp '2022-09-11 12:00:00' -
						   timestamp '2020-01-01 00:00:00')
								));
			temp_id := (select floor(random()*(10-1+1))+1);
			insert into vaccinationhistory(user_id, vaccination_id, date_taken) 
			values(current_user_id, temp_id,random_date_time);
		END LOOP;
		-- Generate closecontacts
		temp_int := (select count(id) from infectionhistory ih where ih.user_id = (select current_user_id));
		if temp_int > 0 then
			ballot := (select floor(random()*(200-0+1))+0);
			for i in 1..ballot LOOP
				temp_user_id := (select w.id from users w where w.id <> (select current_user_id) order by random() limit 1);
				random_date_time := (
					select timestamp '2020-01-01 00:00:00' +
				   random() * (timestamp '2022-09-11 12:00:00' -
							   timestamp '2020-01-01 00:00:00')
									);
				temp_int := (select floor(random()*(100-1+1))+1);
				BEGIN
					insert into closecontacts(infected_user_id, contacted_user_id, contact_timestamp, rssi) 
					values(current_user_id, temp_user_id, random_date_time, temp_int);
				EXCEPTION WHEN check_violation THEN
					raise notice '% %', SQLERRM, SQLSTATE;
				END;
			END LOOP;
		end if;
		-- raise notice 'Value: %', row;
	END LOOP;
end;$$
