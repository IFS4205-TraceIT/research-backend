# Anonymization
## Requirements
1. Synth data generator
2. python version 3
3. postgresql

## Understanding how to use
1. Generate dummy data
2. Run the anonymizer script
3. View data om research database

## Setting up 
The files to be customized and changed are ```anonymizer_script.py``` for database connection. The 2 database name used are ```traceit_test``` and ```traceit_research_test```.
1. Create the 2 databases ```traceit_test``` and ```traceit_research_test```
2. Edit the file ```anonymizer_script.py``` and change the global variable of ```maindb``` and ```researchdb``` to suit your database connection settings.
3. Edit the file ```sampledata/traceit_test/users.json``` of the sttings on ```constant```, change the constant to the amount of users you want to generate. 

## Generating test data
1. Execute the ```init_statement.sql``` in sampledata. This will create all tables used for the main system database.
2. Copy the ```traceit_test``` folder into your synth workspace.
3. Using synth, generate the data for Users and VaccinationTypes.
```
synth generate traceit_test/ --to postgres://postgres:<password>@<IP address>:5432/traceit_test
```
4. Alter the id column to uuid type by executing the ```alter_statement.sql```
5. Execute the ```generate_relations.sql``` which will populate the rest of the secondary tables.
6. You should have a bunch of data, you can clarify by running ```select * from researchdata```, which is a view made for the anonymize process.

## Anonymizing the data with k-anonymity
1. Using python3, run the ```anonymizer_script.py```
```
python3 anonymizer_script.py
```
2. The result should be reflected in the research database.
