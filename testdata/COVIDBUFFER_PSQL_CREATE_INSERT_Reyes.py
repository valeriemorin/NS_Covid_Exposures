# Import libraries to work with our spatial data
import psycopg2
import pandas as pd
#Connect to the PSQL Server
password = input("Enter your Password: ")
conn = psycopg2.connect(host = 'localhost',
                       port=5432,
                       database="postgres",
                       user='postgres',
                       password=password)

#create a curosor
cr_cur = conn.cursor()
# Create POSTGIS Extension
postgis = 'CREATE EXTENSION postgis;'
try:
    cr_cur.execute(postgis)
except:
    print("Connection already established")

#create a curosor
cr_cur = conn.cursor()

# Creating Covid_Data Tables
#We create two strings to be executed.
#First string DROPS the table if it already exists (initialize)
drop_string = "DROP TABLE IF EXISTS COVID_BUFFERS"
#Create string to be inserted to make COVID_BUFFERS table.
cr_string = "CREATE TABLE COVID_BUFFERS (objectid NUMERIC(5) NOT NULL UNIQUE,\
                                Place varchar (255),\
                                Day varchar(3),\
                                DateofExposure DATE,\
                                TimeofExposure varchar(25),\
                                Address varchar(255),\
                                Zone varchar(10),\
                                LastUpdated varchar(40),\
                                ExposureArea varchar(255),\
                                GeolocationAddress varchar(255),\
                                latlong geometry('POINT',0,2),\
                                bufferdistance NUMERIC(2,1),\
                                shapelength NUMERIC,\
                                shapearea NUMERIC);"

# Function to complete transactions.
# Complete the transaction
def execute_commit():
    cr_cur.execute("""commit""")

### Call the function and commit, create the table.
execute_commit()
cr_cur.execute(drop_string)
execute_commit()
cr_cur.execute(cr_string)

### Read the Data and Display
covid_zones = pd.read_csv('buffers_database.csv')
### Read the .csv file and prepare file for INSERT statements:

##Create observations variable to store our data and iterate through.
buffer_observations = []  
infile = open("buffers_database.csv", "r")
line = infile.readline()
#Iterate over every line in the .csv file
while line != "":
    line = line.rstrip('\n')
    buffer_observations.append(line.split(","))
    line = infile.readline()
infile.close()

def insert_string_execute(ins_str):
    cr_cur = conn.cursor()
    cr_cur.execute(ins_str)
    
for case in buffer_observations[1:]:
    insert_string = "INSERT INTO COVID_BUFFERS VALUES" \
    "("+case[0]+","\
    "'"+case[1]+"'"+"," \
    "'"+case[2]+"'"+"," \
    "'"+case[3].strip(" ")+"'"+","\
    "'"+case[4].strip(" ")+"'"+","\
    "'"+case[5]+"'"+"," \
    +"'"+case[6]+"'"+"," \
    +"'"+case[7]+"'"+"," \
    +"'"+case[8]+"'"+"," \
    +"'"+case[9]+"'"+"," \
    +"ST_GeomFromText('Point(" +str(case[10])+" "+str(case[11])+")',4326)"+"," \
    +"'"+case[12]+"'"+"," \
    +"'"+str(float(case[13]))+"'"+"," \
    +"'"+str(float(case[14]))+"')" 
    insert_string_execute(insert_string)
    execute_commit()


### Check to see if the data was imported properly
### Queries: SELECT statements
def execute_select(select_str):
    cr_cur = conn.cursor()
    cr_cur.execute(select_str)
    return cr_cur.fetchall()


select_string1 = "SELECT * FROM COVID_BUFFERS"
results = execute_select(select_string1)

number = int(input("How many results do you want to print to the terminal?: "))
for result in results[0:number]:

    print(result)
    print("\n")


conn.close()