
import camelot
import pandas as pd
import PyPDF2
import numpy as np
import glob
from helpers.tools.table_utils import remove_empty_columns, remove_empty_rows, table_regex
from pathlib import  PureWindowsPath
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

    table.df=df
    #remove /n in the header

    for column in table.df:
        table.df[column] = table.df[column].str.replace('\n','')
        
    #remove the first row
    table.df = table.df.drop(table.df.index[0])
    return table


def remove_table(table):
    table=table.df
    if table.empty:
        return None 
    elif len(table.columns) == 1 or len(table.columns) == 2:
        return None
    elif table_regex(table,"PART  NUMBER"):
        table=table.replace('', np.nan).groupby(0).first().reset_index()
        return table
    elif table_regex(table,"PRODUCTNO"):
        table=table.replace('', np.nan).groupby(0).first().reset_index()

        return table
    elif table_regex(table, "PIEZA"):
        table=table.replace('', np.nan).groupby(0).first().reset_index()
        return table
    elif table_regex(table, "DESCRIPCION"):
            table=table.replace('', np.nan).groupby(0).first().reset_index()

    return None
def getPages(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    return num_pages

def getTables(filename):
        #C:\Users\javie\OneDrive\Documentos\easy\pdfs\javier.alejandro.flores.2@gmail.com\2022-10-03_14-12-29_7.pdf
        filename = PureWindowsPath(filename)
        filename = str(filename)
        tables = camelot.read_pdf(filename, pages='1-end', flavor="stream")
        pieces=pd.DataFrame()
        for table in tables:
            table = clean_table(table)
            table = remove_table(table)
            if table is not None:
                table = remove_empty_columns(table)
                table = remove_empty_rows(table)
                pieces = pd.concat([pieces,table])
                
        for index, row in pieces.iterrows():
            insert_item(Quantity_items=row[0],Mesure_items=row[1], Description_items=row[4],Cost_items=row[5])

        return pieces    
                                    
