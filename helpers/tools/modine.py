import os
from pathlib import PureWindowsPath
import camelot
from numpy import fix
import pandas as pd
import PyPDF2
import glob
import numpy as np
from helpers.tools.table_utils import *


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

def remove_table(table,filename):
    table=table.df
    #tble has 2 columns return none 
    
    if  len(table.columns) == 2:
        tables = camelot.read_pdf(filename, pages='1-end', flavor="stream",table_areas=["17,539,591,199"])
        for table in tables:
            if table.df is not None:
                table=clean_table(table)
                table=table.df
                if table is not None:
                    #if table only has 3 rows return none
                    if len(table.index) == 3:
                        #remove 2 rows from the top
                        table=table.drop(table.index[0:2])
                        table=table.drop(table.columns[0],axis=1)
                        
                        table=table.reset_index(drop=True)
                        table=table.drop(table.columns[0],axis=1)

                        if len(table.columns) == 7:
                            table.columns = ["Peso","Cantidad","UM","Descripccion"," Unitario","Pais","Valor Total"]
                        elif len(table.columns) == 6:
                            table.columns = ["Peso","Cantidad","UM","Descripccion"," Unitario","Valor Total"]
                        elif len(table.columns) == 5:
                            table.columns = ["Peso","Cantidad","UM","Descripccion","Valor Total"]
 
                        print(table)
                        return table
                    else:
                        #remove 3 rows from the top and 0 column from the lef 
                        table=table.drop(table.index[0:6])
                        table=table.drop(table.columns[0],axis=1)
                        table=table.reset_index(drop=True)
                        print(table)
                        return table
                   
    elif not table_regex(table,"MODINE"):
        #remover 2 rows from the top 
        table=table.drop(table.index[0:2])
        if table.iloc[0,0]=="NUMERO" or table.iloc[0,0]=="CLASE" or table.iloc[0,0]=="NUMEROCLASEBRUTO":
            #remove 0 column
            table=table.drop(table.columns[0],axis=1)
            table=table.drop(table.index[0:1])
        return table


    return None
def getPages(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    return num_pages

def getTables(filename):
 

        filename = PureWindowsPath(filename)
        filename = str(filename)
        tables = camelot.read_pdf(filename, pages='1-end', flavor="stream")
        pieces=pd.DataFrame()
        #check tables has dataframe
        for table in tables:
                if table.df is not None:
                    table=clean_table(table)
                    table=remove_table(table,filename)
                    if table is not None:
                        #reset index
                        table=table.reset_index(drop=True)
                        pieces=pd.concat([pieces,table]) 
                        
        return pieces                

                