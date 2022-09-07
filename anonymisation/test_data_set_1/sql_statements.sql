-- Create tables / Reset tables
drop table if exists medicals, patients;

create table patients(
	id serial primary key,
	name text,
	dob date,
	zip_code integer
);

create table medicals(
	id serial primary key,
	user_id integer references patients(id),
	code integer
);
----
-- View all data connected with Users and thier medical records
select p.name, p.dob, p.zip_code, m.code 
from patients p, medicals m
where p.id = m.user_id
;
----
-- Count the current k anonymity of a single column
select p.dob, count(*) as k
from patients p
group by p.dob
having count(*) < 3;
----