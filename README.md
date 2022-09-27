# research-backend

# Connecting to postgreSQL server
1. Edit the pg_hba.conf on the machine hosting the postgreSQL server.
2. Add the following line into the file to allow connections to the server.
```host    all             all            <IP addr of server>          scram-sha-256```


# Research django web backend

## Setting up for local development

> Do view the settings file in `research_backend/settings.py` to modify any settings before starting.

1. Ensure you have the following installed:
    * Python: `3.10` or above
    * Docker: `20.10.18` or above
    * Docker Compose:  `2.10.2` or above
2. Setup the required services using the `docker-compose.yml` file:
    ```bash
    docker-compose up
    ```
3. Installing dependencies:
    1. Install poetry on your machine: https://python-poetry.org/
    2. Run `poetry install` to install the required dependencies.
4. Set and export the required environment variables:
    ```bash
    export DJANGO_SECRET_KEY="test" \
        DJANGO_DEBUG="True" \
        VAULT_ADDR="http://127.0.0.1:8200" \
        VAULT_TOKEN="dev-only-token" \
        POSTGRES_HOST="127.0.0.1" \
        POSTGRES_PORT="5432" \
        POSTGRES_DB="test1" \
        POSTGRES_RESEARCH_DB="test2" \
        POSTGRES_USER="test" \
        POSTGRES_RESEARCH_USER="test2" \
        POSTGRES_PASSWORD="test" \
        POSTGRES_RESEARCH_PASSWORD="test2"
    ```

5. Run `poetry run python manage.py makemigrations` and `poetry run python manage.py migrate` to migrate the database.
6. Run `poetry run python manage.py runserver` to start the server.

# Anonymization and Sample Data
1. Run `poetry run python anonymisation/sampledata/generate.py` to generate initial data for testing purposes.
2. Run `poetry run python anonymisation/anonymizer_script.py` to start anonymizing process.