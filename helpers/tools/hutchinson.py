
from pathlib import PureWindowsPath
import camelot
import pandas as pd
import PyPDF2
import glob
import numpy as np
from helpers.tools.table_utils import regex_all_table, table_regex

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

def remove_not_data(table):
    #remove the first row
    table = table.drop(table.index[0])
    #remove the last row
    table = table.drop(table.index[-1])
    table = table.reset_index(drop=True)
    if table.iloc[0,0].startswith('Pelicanos') or table.iloc[0,0].startswith('HENRI-FABRE'):
        return None
    elif table.iloc[0,0].startswith('Transporte') or table.iloc[0,0].startswith(' 260 HUDSON RIVE'):
        return None
    elif table.iloc[0,0].startswith('PELICANOS') or table.iloc[0,0].startswith('9630 NORWALK BLVD'):
        return None
    elif table.iloc[0,0].startswith('Importador') or table.iloc[0,0].startswith('. P. O. BOX 894'):
        return None
    elif table.iloc[0,0].startswith('150 SALES AVENU') or table.iloc[0,0].startswith(' 260 HUDSON RIVER'):
        return None
    
    table=table.replace(' ', np.nan).groupby(0).first().reset_index()

    return table

def detect_orientation(filename):
    pdf = PyPDF2.PdfFileReader(open(filename, 'rb'))
    page = pdf.getPage(0).mediaBox
    if page.getUpperRight_x() - page.getUpperLeft_x() > page.getUpperRight_y() - page.getLowerRight_y():
        return 'landscape'
    else:
        return 'portrait'
def getPages(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
    num_pages = pdfReader.numPages
    return num_pages
def getTables(filename):
    
    filename = PureWindowsPath(filename)
        
    filename = str(filename)        
    tables = camelot.read_pdf(filename, flavor='stream', pages='1-end',split_text=True)
    for table in tables:
        if  not table.df.empty:
                table=clean_table(table)
                table=remove_not_data(table.df)
                
            
                                        
    return tables