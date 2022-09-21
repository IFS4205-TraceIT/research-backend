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
	infectionhistory_id integer references InfectionHistory(id)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	constraint different_user check(
		infected_user_id <> contacted_user_id
	)
);








