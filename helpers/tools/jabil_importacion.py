import tabula
import pandas as pd
import re
import numpy as np
from helpers.tools.table_utils import umc_values, get_num_pages, index_containing_substring
from db_custom import insert_item
def create_column_name(parts):
    name = ''
    for part in parts:
        part = str(part)
        if 'nan' in part or 'Unnamed' in part:
            continue
        name += f' {part}'
    return name.strip()


def extract_pieces_data(pieces, pieces_clean):
    if 'UMC' in pieces_clean.columns:
        return pieces_clean
    
    data = pieces['DESCRIPCION']
    rows = data[data.str.contains('^(?:[\d|,|\.]+)\s+(?:[A-Z]+)\s+\$(?:[\d|,|.]+)$')]
    parts = rows.str.extract('^([\d|,|\.]+)\s+([A-Z]+)\s+\$([\d|,|.]+)$')
    pieces_clean['CANTIDAD'] = parts[0].to_list()
    pieces_clean['UMC'] = parts[1].to_list()
    pieces_clean['COSTO UNIT'] = parts[2].to_list()
    
    return pieces_clean


def separate_description(pieces_clean):
    try:
        umc_extraction = pieces_clean['DESCRIPCION'].str.extract(f'({" | ".join(umc_values)})', expand=False)
        if umc_extraction.isnull().all():
            return pieces_clean

        parts = pieces_clean['DESCRIPCION'].str.split(' | '.join(umc_values), expand=True)
        extracted = parts[0].str.extract('(\D*)(\d|,|.*)$')
        pieces_clean['DESCRIPCION'] = extracted[0]
        pieces_clean['CANTIDAD'] = extracted[1]
        pieces_clean['UMC'] = umc_extraction
        pieces_clean['COSTO UNIT'] = parts[1]

        return pieces_clean
    except Exception:
        return pieces_clean


# Clean columns
def clean_columns(pieces):
    old_columns = ['' if 'Unnamed' in x else x for x in pieces.columns[:].tolist()]
    new_columns = [create_column_name(x) for x in zip(old_columns,pieces.iloc[0,:])]
    new_columns[-1] = 'TOTAL DOLARES'
    new_columns[-2] = 'TD2'
    new_columns[0] = 'TIPO Y CANTIDAD'
    new_columns[1] = 'PESO BRUTO'
    new_columns[2] = 'PESO NETO'
    
    pieces.columns = new_columns
    pieces['TIPO Y CANTIDAD'] = pieces.loc[:, 'TIPO Y CANTIDAD'].fillna('')
    if 'CODIGO DE PERMISO'  in pieces.columns:
        pieces['CODIGO DE PERMISO'] = pieces.loc[:, 'CODIGO DE PERMISO'].fillna('')
    pieces = pieces.dropna(how='all', axis=1)
    new_columns = pieces.columns.to_list()
    new_columns[3] = 'DESCRIPCION'
    pieces.columns = new_columns

    pieces = pieces.iloc[1: , :]
    while 'DOLARES' in str(pieces.iloc[0,-1]) or 'DOLARES' in str(pieces.iloc[1,-1]) or 'VALOR' in str(pieces.iloc[0,-1]) or 'VALOR' in str(pieces.iloc[1,-1]):
        pieces = pieces.iloc[1: , :]

    pieces_clean = pieces[pieces['PESO NETO'].notna()].copy()
    pieces_clean = pieces_clean[pieces_clean['DESCRIPCION'].notna()]

    if 'TD2' in pieces_clean.columns:
        pieces_clean['TD2'] = pieces_clean.loc[:, 'TD2'].fillna('')
        pieces_clean['TOTAL DOLARES'] = pieces_clean.loc[:, 'TOTAL DOLARES'].fillna('')
        pieces_clean["TOTAL DOLARES"] = pieces_clean["TD2"].astype(str)  + ' ' + pieces_clean["TOTAL DOLARES"].astype(str)
        del pieces_clean['TD2']
    
    
    
    pieces_clean = pieces_clean.dropna(how='all', axis=1)
    
    return pieces_clean, pieces

def extract_from_pdf(filename):
    data_pieces_clean = [pd.DataFrame()]
    data_pieces = [pd.DataFrame()]
    tables_full = tabula.read_pdf_with_template(input_path=filename,
        template_path="helpers/templates/jabil_importacion/Jabil Importacion P1.tabula-template.json")

    for idx, table in enumerate(tables_full):
        try:
            result_clean, result = clean_columns(table)
            data_pieces_clean.append(result_clean)
            data_pieces.append(result)
        except:
            raise("error cannot extract")

    pieces_clean = pd.concat(data_pieces_clean).reset_index(drop=True)
    pieces = pd.concat(data_pieces)  
    return pieces_clean, pieces

def extract_data_jabil_import(filename):
    pieces_clean, pieces = extract_from_pdf(filename)
    pieces_clean = pieces_clean.iloc[:-1,:]
    pieces_clean = separate_description(pieces_clean)
    pieces_clean = extract_pieces_data(pieces, pieces_clean)
   
    for index, row in pieces_clean.iterrows():
        insert_item(row['DESCRIPCION'],row['CANTIDAD'],row['UMC'],row['COSTO UNIT'])
    return pieces_clean

# filename = 'facturas/jabil_importacion/15.pdf'
# result = extract_data(filename)
# print(result)