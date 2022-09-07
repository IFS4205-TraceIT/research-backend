# research-backend

# Connecting to postgreSQL server
1. Edit the pg_hba.conf on the machine hosting the postgreSQL server.
2. Add the following line into the file to allow connections to the server.
```host    all             all            <IP addr of server>          scram-sha-256```

# Anonymization
## Setting up test data
0. Run the SQL statement provided in the ```test_data_set folders``` to create the relevant tables for testing
1. Install synth (from link: https://www.getsynth.com/)
2. Create a workspace folder and perform a synth init in the folder
```mkdir workspace && cd workspace && synth init```
3. Create a app (preferbly the database name)
```mkdir <database name>```
4. Copy the json files from the ```test_data_set folders``` into the app folder
5. Run the following command to upload the generated data into postgreSQL
```
synth generate <app name>/ --size 50 --to postgres://postgres:<password>@<IP address>:5432/<database name>
```
Example:
```
synth generate traceit_test/ --size 50 --to postgres://postgres:password@192.168.1.8:5432/traceit_test
```
