DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

DROP table if exists CloseContacts, Notifications, InfectionHistory, VaccinationHistory, BuildingAccess, Users, Buildings, VaccinationTypes, ContactTracers;

create table Users(
	id text primary key,
	nric text UNIQUE not NULL,
	name text not null,
	dob date not null,
	email text,
	phone INTEGER not null,
	gender text not null,
	address text not null,
	postal_code text not null
);

create table Buildings(
	id serial primary key,
	name text not null,
	location integer not null
);

create table BuildingAccess(
	id serial primary key,
	user_id text references Users(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	building_id integer references Buildings(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	access_timestamp TIMESTAMP not null,
	unique(user_id, building_id, access_timestamp)
);

create table VaccinationTypes(
	id serial primary key,
	name text not null,
	start_date date not null
);

create table VaccinationHistory(
	id serial primary key,
	user_id text references Users(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	vaccination_id integer references VaccinationTypes(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	date_taken date not null,
	unique(user_id, vaccination_id, date_taken)
);

create table InfectionHistory(
	id serial primary key,
	user_id text references Users(id)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	recorded_timestamp TIMESTAMP not null,
	unique(user_id, recorded_timestamp)
);

create table ContactTracers(
	id text primary key
);

create table Notifications(
	due_date date,
	start_date date,
	tracer_id text references ContactTracers(id)
		ON DELETE SET NULL
		ON UPDATE CASCADE,
	infection_id integer references infectionhistory(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	uploaded_status boolean default FALSE,
	primary key(infection_id)
);

create table CloseContacts(
	id serial primary key,
	infected_user_id text references Users(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	contacted_user_id text references Users(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	contact_timestamp timestamp not null,
	rssi numeric not null,
	unique(infected_user_id, contacted_user_id, contact_timestamp),
	constraint different_user check(
		infected_user_id <> contacted_user_id
	)
);

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







