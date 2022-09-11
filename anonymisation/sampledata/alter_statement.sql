drop view if exists researchdata;

ALTER TABLE closecontacts 
drop constraint closecontacts_infected_user_id_fkey,
drop constraint closecontacts_contacted_user_id_fkey,
ALTER COLUMN infected_user_id SET DATA TYPE uuid using infected_user_id::uuid,
ALTER COLUMN contacted_user_id SET DATA TYPE uuid using contacted_user_id::uuid;

ALTER TABLE buildingaccess
drop constraint buildingaccess_user_id_fkey,
ALTER COLUMN user_id SET DATA TYPE uuid using user_id::uuid;

ALTER TABLE infectionhistory
drop constraint infectionhistory_user_id_fkey,
ALTER COLUMN user_id SET DATA TYPE uuid using user_id::uuid;

ALTER TABLE vaccinationhistory
drop constraint vaccinationhistory_user_id_fkey,
ALTER COLUMN user_id SET DATA TYPE uuid using user_id::uuid;

ALTER TABLE users
  ALTER COLUMN id SET DATA TYPE uuid using id::uuid;

alter table closecontacts 
ADD constraint closecontacts_infected_user_id_fkey
foreign key (infected_user_id) references users (id),
ADD constraint closecontacts_contacted_user_id_fkey
foreign key (contacted_user_id) references users (id);

alter table buildingaccess
ADD constraint buildingaccess_user_id_fkey
foreign key (user_id) references users (id);

alter table infectionhistory
ADD constraint infectionhistory_user_id_fkey
foreign key (user_id) references users (id);

alter table vaccinationhistory
ADD constraint vaccinationhistory_user_id_fkey
foreign key (user_id) references users (id);

drop view if exists researchdata;
create or replace view researchdata as (
	select u.dob, u.gender, u.postal_code, 
	ARRAY(
		select vt.name 
		from vaccinationtypes vt, vaccinationhistory vh
		where vh.vaccination_id = vt.id and vh.user_id = u.id
	) as list_of_vaccines,
	(
		select date(max(cc.contact_timestamp))
		from closecontacts cc
		where cc.contacted_user_id = u.id
	) as last_close_contact,
	(
		select date(max(ih.recorded_timestamp))
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

