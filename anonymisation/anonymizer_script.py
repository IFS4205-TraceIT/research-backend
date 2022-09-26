import psycopg2
import os
import csv
import pandas as pd
from datetime import datetime, date

# Variables used by k-anonymity
k = 3
kalgo = "mondrian"
dataset = "traceit"
basefolder = os.getcwd() + '/anonymisation/'
kanonymityfolder = "kanonymity"
datafolder = basefolder + kanonymityfolder + "/data/"
resultfolder = basefolder + kanonymityfolder + "/results/"

# SQLs files
view_file = "researchdata_view.sql"
researchdb_file = "researchdb.sql"

# Variables used by database
# [ip address, database name, username, password]
maindb = [os.environ['POSTGRES_HOST'],os.environ['POSTGRES_DB'],os.environ['POSTGRES_USER'],os.environ['POSTGRES_PASSWORD']]
researchdb = [os.environ['POSTGRES_HOST'],os.environ['POSTGRES_RESEARCH_DB'],os.environ['POSTGRES_USER'],os.environ['POSTGRES_PASSWORD']]


# Important columns_type = {age, postal, gender}
columns_type = ["age", "gender", "postal", "si", "si", "si", "si", "si", "si"]
columns = ["dob","gender", "postal_code", "list_of_vaccines", "last_close_contact", "last_infected_date", "total_infection", "total_close_contact_as_infected", "total_close_contact_with_infected"]
quasi_identifiers = [0, 1 ,2] # Store them by the array index

def list_to_string(list):
    result = ""
    delim = "/"
    for each in list:
        result += (str(each) + delim)
    return result[:-1]

def filter_data(list):
    result = ""
    for each in list:
        if type(each) == type([]):
            each = list_to_string(each)
        result += str(each)+";"
    return result[:-1]

def write_to_file(result):
    with open(datafolder + dataset + "/" + dataset + '.csv', 'w') as f:
        writer = csv.writer(f)
        # write column headers
        writer.writerow([filter_data(columns)])
        for each in result:
            # write data per row
            writer.writerow([filter_data(each)])

def db_export(conn):
    cur = conn.cursor()
    sql_file = open(basefolder + view_file)
    sql_as_string = sql_file.read()
    cur.execute(sql_as_string)
    result = cur.fetchall()
    write_to_file(result)
    data = pd.DataFrame(result, columns = columns)
    return data

def get_age(data):
    birthDate = datetime.strptime(data, '%Y-%m-%d')
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return abs(age)

def process_age(data):
    process_result = ""
    process_result += ";" + data[:-3]
    age = get_age(data)
    process_result += ";" + str(age)
    process_result += ";" + str(int(age/10) * 10) + "-" + str(((int(age/10) + 1) * 10)-1)
    return process_result
    


def get_hierarchy(data, datatype):
    data = str(data)
    end = ";*"
    result = data
    if datatype == "age":
        result += process_age(data)
    elif datatype == "postal":
        result += ";" + data[:-1] + "*"
        result += ";" + data[:-2] + "**"
        result += ";" + data[:-3] + "***"
        result += ";" + data[:-4] + "****"
        result += ";" + data[:-5] + "*****"
    elif datatype == "gender":
        pass
    else:
        return None
    return result + end

def generate_hierarchy(data):
    for i in quasi_identifiers:
        with open(datafolder + dataset + "/hierarchies/" + dataset + '_hierarchy_' + columns[i] +'.csv', 'w') as f:
            writer = csv.writer(f)
            for each in data[columns[i]].unique():
                result = get_hierarchy(each, columns_type[i])
                writer.writerow([result])
        

def db_con(dbargs):
    conn = None
    try:
        conn = psycopg2.connect(
            host=dbargs[0],
            database=dbargs[1],
            user=dbargs[2],
            password=dbargs[3]
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return None


def clean_db(conn, cur):
    sql_file = open(basefolder + researchdb_file)
    sql_as_string = sql_file.read()
    cur.execute(sql_as_string)
    conn.commit()

def db_import(conn):
    cur = conn.cursor()
    clean_db(conn, cur)

    insert_statement = """
        insert into researchdata
        (dob, gender, postal_code, list_of_vaccines, last_close_contact, last_infected_date, total_infection, total_close_contact_as_infected, total_close_contact_with_infected) 
        values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    with open(resultfolder + dataset + "/" + kalgo + "/" + dataset + "_anonymized_" + str(k) + ".csv",'r') as f:
        next(f)
        reader = csv.reader(f)
        for each in reader:
            temp = tuple(each[0].split(";"))
            cur.execute(insert_statement,temp)
            conn.commit()
            

def main():
    conn = db_con(maindb)
    if(conn == None):
        exit(1)
    
    # Get data from database into a csv file
    data = db_export(conn)
    conn.close()
    # Create generalization hierarchy files
    generate_hierarchy(data)

    # k-anonymity by kaylode
    kanon_args = "--method="+ kalgo +" --k="+str(k)+" --dataset="+dataset
    wdir = os.getcwd()
    os.chdir(basefolder + kanonymityfolder)
    os.system("python3 anonymize.py "+kanon_args)
    os.chdir(wdir)

    # Gather anonymized data in results and add to research database
    conn = db_con(researchdb)
    db_import(conn)
    conn.close()
    

if __name__ == '__main__':
    main()