import sys
import re
import psycopg2
import csv
from email_validator import validate_email, EmailNotValidError

def create_table():
    sql = '''CREATE TABLE USERS(name CHAR(20),surname CHAR(20),email CHAR(100) UNIQUE)'''
    return sql

all_arguments = " ".join(sys.argv)
filename = re.search("--file .* ", all_arguments).group().split(" ")[1]
username = re.search("-u .*", all_arguments).group().split(" ")[1]
pass_ = re.search("-p .*", all_arguments).group().split(" ")[1]
host_ = re.search("-h .*", all_arguments).group().split(" ")[1]
sql_table = create_table()


def dry_run():
    print("executed dry run")

def full_run():
    #insert table
    conn = psycopg2.connect(user=username, password=pass_, host=host_, port= '5432')
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    #Doping EMPLOYEE table if already exists.
    cursor.execute("DROP TABLE IF EXISTS USERS")
    cursor.execute(sql_table)

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name_value = str(row[0].capitalize())
            surname_value = str(row[1].capitalize())
            email_value = str(row[2].lower())
            regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
            #if (re.fullmatch(regex, email_value)):
            try: 
                validate_email(email_value)
                cursor.execute("INSERT INTO users(name, surname, email) VALUES (%s, %s,%s) ON CONFLICT DO NOTHING;", (name_value, surname_value, email_value))
            except EmailNotValidError as e:
                print("Error: email is invalid! no db insertion has been made")
                

    conn.commit()
    #Closing the connection
    conn.close()


if "--help" in sys.argv and len(sys.argv) == 2:
    print("--file [csv file name] – this is the name of the CSV to be parsed \n--create_table – this will cause the PostgreSQL users table to be built (and no further action will be taken)\n--dry_run – this will be used with the --file directive in case we want to run the script but not insert into the DB. All other functions will be executed, but the database won't be altered\n-u – PostgreSQL username\n-p – PostgreSQL password\n-h – PostgreSQL host")
elif "--file" in sys.argv and "--create_table" in sys.argv and "-u" in sys.argv and "-p" in sys.argv and "-h" in sys.argv and len(sys.argv) <= 12:
    if "--dry_run" in sys.argv:
        dry_run()
    else:
        full_run()
else:
    print("Could not run script. Incorrect arguments provided")