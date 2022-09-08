import psycopg2
import os
import csv
import pandas as pd

# Variables used by k-anonymity
k = 3
dataset = "traceit"
datafolder = "./k-anonymity/data/"

# Variables used by database
maindb = ["localhost","traceit_test","postgres","password"]
researchdb = ["localhost","traceit_research_test","postgres","password"]

tables = ["patients","medicals"]
columns = ["id","name","dob","zip_code", "code"]
columns_type = ["integer", "text", "age", "postal", "integer"]
quasi_identifiers = [2,3] # Store them by the array index

query = """
    select p.id, p.name, p.dob, p.zip_code, m.code 
    from patients p, medicals m
    where p.id = m.user_id
"""

def filter_data(list):
    result = ""
    for each in list:
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
    cur.execute(query)
    result = cur.fetchall()
    write_to_file(result)
    data = pd.DataFrame(result, columns = columns)
    return data

def get_hierarchy(data, datatype):
    if datatype == "age":
        pass
    elif datatype == "postal":
        pass
    elif datatype == "gender":
        pass
    else:
        return None

def generate_hierarchy(data):
    for i in quasi_identifiers:
        for each in data[columns[i]].unique():
            print(each)
            get_hierarchy(each, columns_type[i])
        

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
    kanon_args = "--method=mondrian --k="+str(k)+" --dataset="+dataset
    os.system("python3 ./k-anonymity/test.py "+kanon_args)

    # Gather anonymized data in results and add to research database

    

if __name__ == '__main__':
    main()