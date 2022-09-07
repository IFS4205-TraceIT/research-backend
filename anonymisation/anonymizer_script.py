import psycopg2

host = "localhost"
database = "traceit_test"
user = "postgres"
password = "password"

def db_con():
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return None


    

def main():
    conn = db_con()
    if(conn == None):
        exit(1)
    print("Hello\n")
    conn.close()

if __name__ == '__main__':
    main()