import psycopg2
import psycopg2.extras

# Database details with NAME , USER , PASSWORD , IP ADDRESS
DB_HOST = "ec2-34-233-157-9.compute-1.amazonaws.com"
DB_NAME = "d3ocn5tke718ih"
DB_USER = "qitctylhwyrvsh"
DB_PASS = "c4e09c9c2cb9e8dcf1c85210e6d758e19e5963b0425fff1458673e18261f10aa"

# Connecting postgresql database to the python

conn = psycopg2.connect(
                        dbname=DB_NAME, 
                        user=DB_USER,
                        password=DB_PASS, 
                        host=DB_HOST
                                    )
Status = "DATABASE CONNECTED SUCCESSFULLY"
print(Status)
SQL = conn.cursor()
        
    



