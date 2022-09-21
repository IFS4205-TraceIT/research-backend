import subprocess
import psycopg2
import os

folder_name = "traceit_test"
db = ["192.168.1.9","5432","traceit_test","postgres","password"]

def synth_generate():
    os.system("synth init")
    #postgres://postgres:password@192.168.1.9:5432/traceit_test
    os.system("synth generate "+ folder_name +"/ --to postgres://"+ db[3] +":"+ db[4] +"@"+ db[0] + ":" +db[1] +"/"+db[2])

def execute_sql(conn, filename):
    sql_file = open(filename)
    sql_as_string = sql_file.read()
    cursor = conn.cursor()
    cursor.execute(sql_as_string)
    conn.commit()

def db_con(dbargs):
    conn = None
    try:
        conn = psycopg2.connect(
            host=dbargs[0],
            database=dbargs[2],
            user=dbargs[3],
            password=dbargs[4]
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return None

def main():
    conn = db_con(db)
    if(conn == None):
        exit(1)
    # Generate initial tables
    execute_sql(conn, "init_statement.sql")
    # Generate data for primary tables
    synth_generate()
    # Alter structure of tables to fit uuid
    execute_sql(conn, "alter_statement.sql")
    # Generate secondary tables data
    execute_sql(conn, "generate_relations.sql")
    conn.close()
    

if __name__ == '__main__':
    main()