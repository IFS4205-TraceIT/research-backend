# research-backend

# Connecting to postgreSQL server
1. Edit the pg_hba.conf on the machine hosting the postgreSQL server.
2. Add the following line into the file to allow connections to the server.
```host    all             all            <IP addr of server>          scram-sha-256```

# Anonymization
Refer to the folder ```anonymisation```

# Research django web backend