from multiprocessing import connection
import os 
import pyodbc
from dotenv import load_dotenv
load_dotenv()


Host=os.getenv("HOST")
User=os.getenv("USER")
Password=os.getenv("PASS")
Database=os.getenv("DATABASE")

try:
    connection=pyodbc.connect(Driver='{ODBC Driver 17 for SQL Server}',Server=Host,Database=Database,UID=User,PWD=Password)
except:
    print("Error")
    pass
