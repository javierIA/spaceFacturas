import os 
import pyodbc
from dotenv import load_dotenv
load_dotenv()


Host=os.getenv("HOST")
User=os.getenv("USER")
Password=os.getenv("PASS")
Database=os.getenv("DATABASE")

try:
    dbconection=pyodbc.connect(Driver='{ODBC Driver 17 for SQL Server}',Server=Host,Database=Database,UID=User,PWD=Password)
    print("Connection to database successful")
except Exception as e:
    print(e)
    print("Connection to database failed")
    pass
