from pathlib import PureWindowsPath
import camelot
import pandas as pd
import PyPDF2
import glob
import numpy as np
import tabula
from helpers.tools.table_utils import remove_empty_columns, remove_empty_rows, table_regex,row_contains_word
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


def getPages(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
    num_pages = pdfReader.numPages
    return num_pages

def WockerInvoices(pdfpath):
    
    
    #tables=camelot.read_pdf(pdfpath, pages='1-end',suppress_stdout=False, flavor="stream",table_areas=["55.58723747980614,353.5028573107971,554.3966074313408,135.0540"],split_text=True)
    tables=tabula.read_pdf(pdfpath, stream=True, pages='all',multiple_tables=True,area=[55.58723747980614,353.5028573107971,554.3966074313408,135.0540])
    return tables
def remove_table(table,pdfpath):
    table=table.df
    #if first cell is =="INVOICE SHIP DATE"
    if table_regex(table,"INVOICE SHIP DATE"):
            #Drop the first 3 rows
        table=table.drop(table.index[0:3])
        #reset index
        table=table.reset_index(drop=True)
        #remove empty columns
        table=remove_empty_columns(table)
    if table_regex(table,"MEXICO") or table_regex(table,"Invoice") or table_regex(table,"MEXIC"):
        tables=WockerInvoices(pdfpath)
        
        if len(tables) != 0:
            return tables[0]
        return None
    #if table has 3 row 
    if len(table.index) <3:
        #sumar todas las filas y ponerlas en una sola fila pero matener el nombre de la columna
        table=table.sum(axis=1)
        table=table.to_frame()
        table=table.transpose()
        table=table.reset_index(drop=True)
    if table_regex(table,"item"):
        try:
            table=table.reset_index(drop=True)
            #group by the first column
            table=table.replace(' ', np.nan).groupby(0).first().reset_index()
            
        except:
            table=table.reset_index(drop=True)
        
    return table


    
def getTables(path):
    filename = PureWindowsPath(path)
    filename = str(filename)    
    tables = camelot.read_pdf(filename, pages='1', flavor="stream", table_areas=["34,514,567,194"],split_text=True)
    pieces=pd.DataFrame()
     #check tables has dataframe
    if len(tables) != 0:
            for table in tables:
                if table.df is not None:
                    table=clean_table(table)
                    #table=remove_table(table)
                    if table is not None:
                        pieces=pd.concat([pieces,table.df])
    return pieces  
    
            
                
                                        
                        
