
import os
from dotenv import load_dotenv
from connection import dbconection
load_dotenv()



def execute(sql):
    try:
        with dbconection.cursor() as cursor:
            cursor.execute(sql)
            dbconection.commit()
            return True
    except Exception as e:
        print(e)
        return False
    
def select(sql):
    try:
        with dbconection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except:
        return False


def insert_invoice(Date_invoices,Origin_invoices,Total_invoives,RFC_clients):
    sql = "INSERT INTO invoices (Date_invoices,Origin_invoices,Total_invoices,RFC_clients) VALUES ('{}','{}','{}','{}')".format(Date_invoices,Origin_invoices,Total_invoives,RFC_clients)
    execute(sql) 
    
def insert_item(Description_items,Quantity_items,Mesure_items,Cost_items):
    Num_invoice=getlastidInvoices()
    sql = "INSERT INTO items (Description_items,Quantity_items,Mesure_items,Cost_items,Num_invoice) VALUES ('{}','{}','{}','{}','{}')".format(Description_items,Quantity_items,Mesure_items,Cost_items,Num_invoice)
    execute(sql)
def getlastidItems():
    sql = "SELECT MAX(id_items) FROM items"
    return select(sql)[0][0]
def getlastidInvoices():
    sql = "SELECT MAX(Num_invoices) FROM invoices"
    return select(sql)[0][0]
