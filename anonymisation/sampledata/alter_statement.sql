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


