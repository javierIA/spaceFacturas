from os import sep
import tabula
from PyPDF2 import PdfFileReader
import pandas as pd
import re
import numpy as np
from helpers.tools.table_utils import umc_values, get_num_pages, index_containing_substring
from db_custom import insert_item
def get_num_pages(filename):
    reader = PdfFileReader(filename)
    return reader.numPages

def only_numerics(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))

def use_template_page_one(filename):
    tables_body = tabula.read_pdf_with_template(input_path=filename,
        template_path="helpers/templates/signify/Signify BodyP1.tabula-template.json")

    if any(['PATENTE' in x for x in tables_body[0].columns.to_list()]):
        tables_body = tabula.read_pdf_with_template(input_path=filename,
            template_path="helpers/templates/signify/Signify BodyP1V.tabula-template.json")
    return tables_body

# Clean columns
def clean_columns(pieces):
    old_columns = [str(x) for x in list(pieces.iloc[0,2:])]
    new_columns = ['num', 'descripcion'] + old_columns
    pieces.columns = new_columns
    pieces = pieces.iloc[3: , :]
    pieces = pieces[pieces['num'].notna()]
    pieces_clean = pieces[pieces['descripcion'].notna()].copy()
    while 'nan' in pieces_clean.columns:
        del pieces_clean['nan']
    while 'nan' in pieces.columns:
        del pieces['nan']
    if 'Bultos' in pieces_clean.columns:
        del pieces_clean['Bultos']
    if 'ValorUnitario/ ValorTotal/' in pieces_clean.columns:
        new = pieces_clean['ValorUnitario/ ValorTotal/'].str.split(n=2, expand=True)
        pieces_clean['ValorUnitario/'] = new[0]
        pieces_clean['ValorTotal/'] = new[1]
        del pieces_clean['ValorUnitario/ ValorTotal/']
    return pieces_clean, pieces

def contains_and_drop_total(pieces_clean):
    contains_any = True in pieces_clean['num'].str.contains("Total").to_list()
    if contains_any:
        pieces_clean = pieces_clean[~pieces_clean['num'].str.contains("Total")]
    return pieces_clean, contains_any


def separate_description_column(pieces_clean):
    parts = pieces_clean['descripcion'].str.split('|'.join(umc_values),expand=True, regex=True)
    parts_left = parts[0].str.rsplit(expand=True, n=1)
    parts_right = parts[1].str.split(expand=True)
    umc_extraction = pieces_clean['descripcion'].str.extract(f'({"|".join(umc_values)})', expand=False)
    pieces_clean['parte'] = parts_left[0]
    pieces_clean['cantidad'] = parts_left[1]
    pieces_clean['umc'] = umc_extraction
    if parts_right.empty:
        pieces_clean['fraccion'] = pd.Series()
    else:
        pieces_clean['fraccion'] = parts_right[0]
 
    del pieces_clean['descripcion']
    return pieces_clean

def extract_values_from_text(txt):
    matches = re.search(".*Origin.*: (.*) PREFERENCIA.*: (.*)", txt)
    return matches

def extract_origin_df(pieces):
    pieces_origin = pieces[pieces['descripcion'].isna()]
    pieces_origin = pieces_origin[pieces_origin['num'].notna()]
    pieces_origin = pieces_origin[pieces_origin['num'].str.contains("ORIGEN")]['num'].to_list()
    pieces_origin = [extract_values_from_text(x)[1] for x in pieces_origin]

    return pieces_origin

def extract_pieces_description(pieces):
    
    contains_any = True in pieces['num'].str.contains("Total").to_list()
    if contains_any:
        idx = np.where(pieces['num'].str.contains("Total"))[0][0]
        pieces = pieces.iloc[:idx]
    
    pieces_description = pieces[pieces['num'].notna()].copy()[['num', 'descripcion']]
    pieces_description = pieces_description[~pieces_description['num'].str.contains("ORIGEN")]
    pieces_description = pieces_description[~pieces_description['num'].str.contains("OBSERVACIONES")]
    pieces_description = pieces_description[~pieces_description['num'].str.contains("MODELO")]
    pieces_description = pieces_description[~pieces_description['num'].str.contains("SERIE")]
    g = pieces['descripcion'].notna().cumsum()
    pieces_description = pieces_description.groupby(g[g > 0])['num'].apply(' '.join).reset_index(drop=True).to_frame()
    full_description = pieces_description['num'].to_list()
    full_description = [' '.join(x.split(' ')[1:]) for x in full_description]
    return full_description

def extract_preference_df(pieces):
    pieces_preference = pieces[pieces['descripcion'].isna()]
    pieces_preference = pieces_preference[pieces_preference['num'].notna()]
    pieces_preference = pieces_preference[pieces_preference['num'].str.contains("ORIGEN")]['num'].to_list()
    pieces_preference = [extract_values_from_text(x)[2] for x in pieces_preference]

    return pieces_preference

def extract_pieces_page_one(filename):
    tables_body = use_template_page_one(filename)

    # Get first dataframe with pieces list
    pieces = tables_body[0]
    pieces_clean, pieces = clean_columns(pieces)
    return pieces_clean, pieces

def extract_pieces_page_n(filename):
    tables_body = tabula.read_pdf_with_template(input_path=filename,
    template_path="templates/signify/Signify BodyPM.tabula-template.json")
    data_pieces_clean = [pd.DataFrame()]
    data_pieces = [pd.DataFrame()]
    for page in range(1, get_num_pages(filename)):
    # Get first dataframe with pieces list
        try:
            contains_description_column = any(['DESCRIPCION' in x for x in tables_body[page].columns.to_list()])
            if len(tables_body[page].columns) > 6 and contains_description_column:
                pieces_n = tables_body[page]
                pieces_clean_n, pieces_n = clean_columns(pieces_n)
                data_pieces_clean.append(pieces_clean_n)
                data_pieces.append(pieces_n)
        except Exception:
            pass
    return pd.concat(data_pieces_clean), pd.concat(data_pieces) 

def extract_data_signify(filename):
    first_pieces_clean, first_data_pieces = extract_pieces_page_one(filename)
    data_pieces_clean = [first_pieces_clean]
    data_pieces = [first_data_pieces]
    n_pieces_clean, n_pieces = extract_pieces_page_n(filename)
    data_pieces_clean.append(n_pieces_clean)
    data_pieces.append(n_pieces)

    pieces_clean = pd.concat(data_pieces_clean)
    pieces = pd.concat(data_pieces)
    pieces_clean = pieces_clean.reset_index(drop=True)
    pieces = pieces.reset_index(drop=True)

    pieces_clean, _ = contains_and_drop_total(pieces_clean)
    pieces_clean = separate_description_column(pieces_clean)
    pieces_clean['origen'] = extract_origin_df(pieces)
    pieces_clean['preferencia'] = extract_preference_df(pieces)
    pieces_clean['descripcion'] = extract_pieces_description(pieces)
    pieces_clean = pieces_clean.reset_index(drop=True)
    for index,row  in pieces_clean.iterrows():
        insert_item(Description_items= row['descripcion'],Quantity_items=row['cantidad'],Mesure_items=row['umc'],Cost_items=row['ValorUnitario/'])
    return pieces_clean

# filename = 'facturas/signify_luminaria/16.pdf'
# result = extract_data(filename)
# print(result)

