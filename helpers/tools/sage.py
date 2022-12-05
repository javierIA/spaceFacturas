from pathlib import PureWindowsPath
import camelot
import pandas as pd
import PyPDF2
from db_custom import insert_item
import numpy as np
from table_utils import remove_empty_columns, remove_empty_rows, table_regex
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
        
    table.df = fix_header(table.df) 
    #remove the first row
    table.df = table.df.drop(table.df.index[0])
    return table

def fix_header(table):
    hearder=["DESCRIPCION","Peso","Cantidad","UM","Valor Unitario","Valor Total","na","na"]
    
    if len(table.columns) == 8:
        table.columns = hearder
    elif len(table.columns) == 7:
        table.columns = hearder[:-1]
    elif len(table.columns) == 6:
        table.columns = hearder[:-2]
        
    return table
def getPages(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
    num_pages = pdfReader.numPages
    return num_pages

def remove_table(table):
    table=table.df
    if table is None:
        return None 
    elif len(table.columns) == 1 or len(table.columns) == 2:
        return None
    elif table_regex(table,"49200 HALYARD DRIVE"):
        #table=table.drop(table.index[0:3])
        #table=table.replace('', np.nan).groupby(0).first().reset_index()
        #slpit columns in two columns with space as separator
        return table
    elif table_regex(table,"PLYMOUTHMIUSA"):
        #remove 3 rows from the top 
        #table=table.drop(table.index[0:3])
        table=table.replace('', np.nan).groupby(0).first().reset_index()
        #create one print whit pixel art
    
        
        table[["Parte","Descripcion"]]=table[0].str.split(" ",n=1,expand=True)
        table [["Cantidad","UM"]]=table[1].str.split(" ",n=1,expand=True)
        

        table["UM"] = table["Cantidad"].str.extract(r'([a-zA-Z]+)', expand=False)
        table["Cantidad"]=table["Cantidad"].str.extract(r'(\d+.\d+)').astype('float')

            
        table[["KG","CostoUnit"]]=table[2].str.split(" ",n=1,expand=True)
        #take 9.25707$4154.660 only numbers to $ 
        try:
            table[["CostoUnit","Dlls"]]=table["CostoUnit"].str.split("$",n=1,expand=True)

        except :
            print("no has $")
        table=table.drop(columns=[0])
        table=table.drop(columns=[1])
        table=table.drop(columns=[2])

        return table
    elif table_regex(table,"Piece") or table_regex(table,"Total") :
        #REMOVE HEADER

        table=remove_empty_columns(table)
        table=table.drop(table.index[0:3])
        table.columns=["Parte","Descripcion","Cantidad","Cantidad KG","UM","CostoUnit"]
        return table
    return None


def extract_with_coordinates(filename):
    table=camelot.read_pdf(filename, flavor='stream', pages='1-end', table_areas=['17.220745799676898,513.013030590723,594.8537620516963,172.53199795149249'])
    
    return table
    
def getTables(filename):
        filename = PureWindowsPath(filename)
        filename = str(filename)
        num_pages = getPages(filename)
        tables = camelot.read_pdf(filename, pages='1-end', flavor="stream")
        pieces=pd.DataFrame()
        #check tables has dataframe
        if len(tables) is not 0:
            for table in tables:
                if table.df is not None:
                    table=clean_table(table)
                    table=remove_table(table)
                    if table is not None:
                        pieces= pd.concat([pieces,table])
                        pieces=remove_empty_columns(pieces)
                        
        for index, row in pieces.iterrows():
            insert_item(Description_items=row["Descripcion"],Cost_items=row["CostoUnit"],Quantity_items=row["Cantidad"],UM_items=row["UM"])
        return pieces           
    
            
                
                                        
