
from pathlib import PureWindowsPath
import camelot
import tabula
from  helpers.tools.table_utils import *
import pandas as pd
from db_custom import insert_item
def clean_table(table):
    df = table.df
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    for column in df:
        df[column] = df[column].str.strip()
    #romove the last row
    df = df.drop(df.index[-1])
    #
    for column in df:
        if column!="TOTAL":
            df[column] = df[column].str.replace(',','')     
    table.df=df
    #remove /n in the header
    
    for column in table.df:
        table.df[column] = table.df[column].str.replace('\n','')
        
    #remove the first row
    table.df = table.df.drop(table.df.index[0])
    return table


    

def pieces_cleaner(table):
    if table_regex(table,"PRICING"):
        table = table.drop(table.index[0])
        table = table.reset_index(drop=True)
        #take the first row
        tableData = table.drop(table.index[1:])
        #take the rest of the table and create one column with all the data the tableData

        tableDescription = table.drop(table.index[0]) 
        tableDescription = tableDescription.reset_index(drop=True)
        tableDescription = tableDescription[0].str.cat(sep=' ')
        tableData[4] = tableDescription
        table=tableData
        header=["Unit_Price","Quantity","UM","Total_Price","Description"]
        if len (table.columns) == 5:
            table.columns = header
        return table
    if table_regex(table,"SHIP DATE"):
        #remove last row
        table = table.reset_index(drop=True)
        header= ["Date","Description","Quantity","Unit_Price","UM"]
        #Join data of 1,2,3 columns and create a new column and remove the 1,2,3 columns
        table[1] = table[1].str.cat(table[2],sep=" ").str.cat(table[3],sep=" ")
        table = table.drop([2,3],axis=1)
        table = table.drop(0,axis=0)
        table.columns = header
        table = table.reset_index(drop=True)
        #all data iin um column is "TON"
        table["UM"] = "TON"
        table = table.drop(table.index[-1])
        return table
    return table
        
        
        
def getTables(path):
    pieces=pd.DataFrame()
    filename = PureWindowsPath(path)
    filename = str(filename)  
    tables = camelot.read_pdf(filename, pages='1-end', flavor='stream',table_areas=["11.450629507660107,507.4383068422732,596.1640053038385,232.13461330127885"])
    for table in tables:
        if  not table.df.empty:
            table = clean_table(table)
            table = pieces_clean(table.df)
            pieces_clean=pd.concat([pieces,table])
    #if header is =Date,Description,Quantity,Unit Unit_Price,UM
    for index,row in pieces_clean.iterrows():
            insert_item(Description_items=row["Description"],Quantity_items=row["Quantity"],Mesure_items=row["UM"],Cost_items=row   ["Unit_Price"])
