import sys
import re

all_arguments = " ".join(sys.argv)
filename = re.search("--file .* ", all_arguments).group().split(" ")[1]
#print(len(sys.argv))

def dry_run():
    print("")

def full_run():
    username = re.search("-u .*", all_arguments).group().split(" ")[1]
    password = re.search("-p .*", all_arguments).group().split(" ")[1]
    host = re.search("-h .*", all_arguments).group().split(" ")[1]
    



if "--help" in sys.argv and len(sys.argv) == 2:
    print("--file [csv file name] – this is the name of the CSV to be parsed \n--create_table – this will cause the PostgreSQL users table to be built (and no further action will be taken)\n--dry_run – this will be used with the --file directive in case we want to run the script but not insert into the DB. All other functions will be executed, but the database won't be altered\n-u – PostgreSQL username\n-p – PostgreSQL password\n-h – PostgreSQL host")
elif "--file" in sys.argv and "--dry_run" in sys.argv and len(sys.argv) == 4:
    dry_run()
elif "--file" in sys.argv and "--create_table" in sys.argv and "-u" in sys.argv and "-p" in sys.argv and "-h" in sys.argv and len(sys.argv) == 10:
    full_run()
else:
    print("Could not run script. Incorrect arguments provided")