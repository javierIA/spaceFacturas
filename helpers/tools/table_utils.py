from PyPDF2 import PdfFileReader
import tabula
import pandas as pd
import re 
umc_values = ['EA', 'SET', 'KGM', 'MTR', 'LT', 'PZS', 'JGO']
def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1


def get_num_pages(filename):
    reader = PdfFileReader(filename)
    return reader.numPages

def only_numerics(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))

def extract_from_pdf(filename, template_one, template_n, clean_columns_fn):
    first_pieces_clean, first_data_pieces = extract_from_pdf_page_one(filename, template_one, clean_columns_fn)
    data_pieces_clean = [first_pieces_clean]
    data_pieces = [first_data_pieces]
    n_pieces_clean, n_pieces = extract_from_pdf_page_n(filename, template_n, clean_columns_fn)
    data_pieces_clean.append(n_pieces_clean)
    data_pieces.append(n_pieces)
    pieces_clean = pd.concat(data_pieces_clean)
    pieces = pd.concat(data_pieces)
    pieces_clean = pieces_clean.reset_index(drop=True)
    pieces = pieces.reset_index(drop=True)

    return pieces_clean, pieces

def extract_from_pdf_page_one(filename, template_path, clean_columns_fn):
    tables = tabula.read_pdf_with_template(input_path=filename, template_path=template_path)
    pieces = tables[0]
    pieces_clean, pieces = clean_columns_fn(pieces)
    return pieces_clean, pieces

def extract_from_pdf_page_n(filename, template_path, clean_columns_fn):
    data_pieces_clean = [pd.DataFrame()]
    data_pieces = [pd.DataFrame()]
    tables = tabula.read_pdf_with_template(input_path=filename, template_path=template_path)
    for page in range(1, get_num_pages(filename)):
        pieces_n = tables[page]
        pieces_clean_n, pieces_n = clean_columns_fn(pieces_n)
        data_pieces_clean.append(pieces_clean_n)
        data_pieces.append(pieces_n)
    return pd.concat(data_pieces_clean), pd.concat(data_pieces)


def table_regex(table,regex):
    #if table contains word in regex return true
    for index, row in table.iterrows():
        for column in table:
            if re.search(regex, str(row[column])):
                return True
            
def row_contains_word(table,word):
    #if the row contains the word return index
    index=[]
    for idx, row in table.iterrows():
        for column in table:
            if word in str(row[column]):
                index.append(idx)
                return index
    return False

def tryiloc(table,column,index):
    try:
        return table.iloc[column][index]
    except:
        return None

def remove_empty_rows(table):
    #remove nah and null rows
    for index, row in table.iterrows():
        if row.isnull().all():
            table = table.drop(index)
    return table
def remove_empty_columns(table):
   #if the column is empty or NAN remove it
    for column in table: 
        if table[column].isnull().all() : 
            table = table.drop(column, axis=1)
    return table
def regex_all_table(table,regex):
    #if table contains word in regex return true
    #create regex contain all the word in the list
    
    regex = '|'.join(regex)
    regex=re.compile(regex)
    for  row in table.iterrows():
        for column in table:
            if re.search(regex, str(row[column])):
                return True
    return False
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
