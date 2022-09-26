import subprocess
import psycopg2
from faker import Faker
import random
import string
import uuid
import os

folder_name = "traceit_test"
basefolder = os.getcwd() + '/anonymisation/sampledata/'
db = [os.environ['POSTGRES_HOST'],os.environ['POSTGRES_PORT'],os.environ['POSTGRES_DB'],os.environ['POSTGRES_USER'],os.environ['POSTGRES_PASSWORD']]

insert_user_sql = """
    INSERT INTO users values(%s,%s,%s,%s,%s,%s,%s,%s,%s);
"""

insert_vaccine_sql = """
    INSERT INTO vaccinationtypes(name,start_date) values(%s,%s);
"""

def synth_generate():
    os.system("synth init")
    #postgres://postgres:password@192.168.1.9:5432/traceit_test
    os.system("synth generate "+ folder_name +"/ --to postgres://"+ db[3] +":"+ db[4] +"@"+ db[0] + ":" +db[1] +"/"+db[2])

def user_generate(conn, total):
    fake = Faker()
    cur = conn.cursor()
    for x in range(total):
        name = fake.name()
        dob = fake.date_of_birth()
        email = name.lower().replace(" ", "")+"@"+fake.domain_name()
        phone = fake.pyint(80000000,99999999)
        gender = random.choice(["Male","Female"])
        address = fake.street_address()
        postal_code = str(random.randint(1, 80)).rjust(2, "0") + str(random.randint(1, 9999)).rjust(4, "0")
        nric = ('T' if dob.year > 2000 else 'S')+str(dob)[2:4] + str(random.randint(1, 99999)).rjust(5, "0") + random.choice(string.ascii_letters).upper()
        id = str(uuid.uuid4())
        try:
            cur.execute(insert_user_sql,(id,nric,name,dob,email,phone,gender,address,postal_code))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    conn.commit()
    cur.close()

def vaccine_generate(conn):
    cur = conn.cursor()
    list_of_vaccines = [
        ["Pfizer-BioNTech",'2020-12-21'],
        ["Moderna",'2021-02-17'],
        ["Sinovac",'2021-10-23'],
        ["Novavax",'2022-02-14']
    ]
    for each in list_of_vaccines:
        try:
            cur.execute(insert_vaccine_sql,(each[0],each[1]))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    conn.commit()
    cur.close()

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
    execute_sql(conn, basefolder + "create_table.sql")
    print("Generating primaries...")
    # Generate data for primary tables
    user_generate(conn, 500)
    vaccine_generate(conn)
    print("Generating relations...")
    # Generate secondary tables data
    execute_sql(conn, basefolder + "generate_relations.sql")
    conn.close()
    

if __name__ == '__main__':
    main()