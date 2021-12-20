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
drop_string = "DROP TABLE IF EXISTS NS_HEALTH_FACILITIES"

cr_string = "CREATE TABLE NS_HEALTH_FACILITIES (objectid NUMERIC(5) NOT NULL UNIQUE,\
                                facilityname varchar (255),\
                                opendatabase_facility_type varchar(50),\
                                provider varchar(50),\
                                street_number varchar(10),\
                                street_name varchar(100),\
                                postal_code varchar(7),\
                                city varchar(255),\
                                province varchar(2),\
                                CensusDefinedName varchar(255),\
                                CensusDefinedId integer,\
                                CensusProvinceID integer,\
                                latlong geometry('POINT',0,2));"

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
covid_data = pd.read_csv('novascotia_health_facilities_database.csv')
### Read the .csv file and prepare file for INSERT statements:

##Create observations variable to store our data and iterate through.
ns_health_facilities = []  
infile = open("novascotia_health_facilities_database.csv", "r")
line = infile.readline()
#Iterate over every line in the .csv file
while line != "":
    line = line.rstrip('\n')
    ns_health_facilities.append(line.split(","))
    line = infile.readline()
infile.close()

###############################################################
########################Insert the Data########################
###############################################################

#Define function to execute string insertion to table.
def insert_string_execute(ins_str):
    cr_cur = conn.cursor()
    cr_cur.execute(ins_str)

###############################################################
#####################INSERT STATEMENTS#########################
###############################################################
#Loop through contents of list ns_health_facilities and append them individually
#Into the 'insert string' variable which is then entered into our function above.
for facility in ns_health_facilities[1:]:
    insert_string = "INSERT INTO NS_HEALTH_FACILITIES VALUES"+"("+facility[0]+"," \
    "'"+facility[1]+"'"+"," \
    "'"+facility[2]+"'"+"," \
    "'"+facility[3]+"'"+"," \
    "'"+facility[4]+"'"+"," \
    "'"+facility[5]+"'"+"," \
    "'"+facility[6]+"'"+"," \
    "'"+facility[7]+"'"+"," \
    "'"+facility[8]+"'"+"," \
    "'"+facility[9]+"'"+"," \
    "'"+facility[10]+"'"+"," \
    "'"+facility[11]+"'"+ "," \
     "ST_GeomFromText('Point(" +str(facility[12])+" "+str(facility[13])+")',4326))" 
    #Insert the string and execute it.
    insert_string_execute(insert_string)
    execute_commit()


### Check to see if the data was imported properly
### Queries: SELECT statements
def execute_select(select_str):
    cr_cur = conn.cursor()
    cr_cur.execute(select_str)
    return cr_cur.fetchall()


select_string1 = "SELECT * FROM NS_HEALTH_FACILITIES"
results = execute_select(select_string1)

number = int(input("How many results do you want to print to the terminal?: '"))
for result in results[0:number]:

    print(result)
    print("\n")


conn.close()