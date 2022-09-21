drop view if exists researchdata;
create or replace view researchdata as (
	select u.dob, u.gender, u.postal_code, 
	ARRAY(
		select vt.name 
		from vaccinationtypes vt, vaccinationhistory vh
		where vh.vaccination_id = vt.id and vh.user_id = u.id
	) as list_of_vaccines,
	(
		select DATE(max(cc.contact_timestamp))
		from closecontacts cc
		where cc.contacted_user_id = u.id
	) as last_close_contact,
	(
		select DATE(max(ih.recorded_timestamp))
		from infectionhistory ih
		where ih.user_id = u.id
	) as last_infected_date,
	(
		select count(*)
		from infectionhistory ih2
		where ih2.user_id = u.id
	) as total_infection,
	(
		select count(*)
		from closecontacts cc3
		where cc3.infected_user_id = u.id
	) as total_close_contact_as_infected,
	(
		select count(*)
		from closecontacts cc4
		where cc4.contacted_user_id = u.id
	) as total_close_contact_with_infected
 	from Users u
);

select * from researchdata;
