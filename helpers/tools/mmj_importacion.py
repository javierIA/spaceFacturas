import tabula
import pandas as pd
import re
import numpy as np
from helpers.tools.table_utils import umc_values, get_num_pages, index_containing_substring

pd.options.mode.chained_assignment = None 

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
    if 'CANTIDAD Y UMC' in pieces_clean.columns:
        return pieces_clean
    
    data = pieces['DESCRIPCION']
    rows = data[data.str.contains('(?:\d[\d|,|\.]*)\s*(?:[A-Z]+)\s+\$?(?:[\d|,|\.]+)\s*$')]
    parts = rows.str.extract('(\d[\d|,|\.]*)\s*([A-Z]+)\s*\$?([\d|,|\.]+)\s*$')
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
    pieces = pieces.dropna(how='all', axis=1)
    
    if 'Unnamed' in pieces.columns[1] and 'Unnamed' in pieces.columns[2]:
        pieces.columns = pieces.iloc[0] 
        pieces = pieces[1:]
    old_columns = ['' if 'Unnamed' in str(x) else x for x in pieces.columns[:].tolist()]
    if old_columns[0].strip() == 'TIPO Y CANTIDAD TOTAL':
        parts = pieces.iloc[:,0].str.extract("^(.*\s)?([\d|,]*\.[\d]*)$")
        pieces = pieces.iloc[:,1:]
        pieces.insert(0, 'PESO BRUTO', parts[1])
        pieces.insert(0, 'TIPO Y CANTIDAD', parts[0])
        old_columns = ['' if 'Unnamed' in str(x) else x for x in pieces.columns[:].tolist()]
    new_columns = [create_column_name(x) for x in zip(old_columns,pieces.iloc[0,:])]
    if new_columns[0].strip() == '':
        new_columns.pop(0)
        pieces = pieces.iloc[:,1:]
        old_columns = ['' if 'Unnamed' in str(x) else x for x in pieces.columns[:].tolist()]
    if new_columns[-1].strip() == '':
        new_columns.pop(-1)
        pieces = pieces.iloc[:,:-1]
        old_columns = ['' if 'Unnamed' in x else x for x in pieces.columns[:].tolist()]
    permission_idx = index_containing_substring(new_columns, 'CODIGO')
    new_columns[-1] = 'TOTAL DOLARES'
    new_columns[-2] = 'TD2'
    new_columns[permission_idx] = 'CODIGO DE PERMISO'
    new_columns[0] = 'TIPO Y CANTIDAD'
    new_columns[1] = 'PESO BRUTO'
    new_columns[2] = 'PESO NETO'

    pieces.columns = new_columns
    if permission_idx == 3:
        pieces.loc[:, 'DESCRIPCION'] = pieces.iloc[:,permission_idx]
        pieces.loc[:, 'CODIGO DE PERMISO'] = ''
    else:
        pieces['DESCRIPCION'] = pieces.iloc[:,3:permission_idx].fillna('').astype(str).agg(' '.join, axis=1)
    retaining = ['TIPO Y CANTIDAD', 'PESO BRUTO', 'PESO NETO', 'DESCRIPCION', 'CODIGO DE PERMISO', 'TOTAL DOLARES']
    if 'TD2' in new_columns:
        retaining.insert(0, 'TD2')

    pieces = pieces[retaining].copy()
    
    pieces.loc[:, 'TIPO Y CANTIDAD'] = pieces.loc[:, 'TIPO Y CANTIDAD'].fillna('')
    if 'CODIGO DE PERMISO'  in pieces.columns:
        pieces['CODIGO DE PERMISO'] = pieces.loc[:, 'CODIGO DE PERMISO'].fillna('')
    
    pieces = pieces.iloc[1: , :]
    while 'DOLARES' in str(pieces.iloc[0,-1]) or 'DOLARES' in str(pieces.iloc[1,-1]) or 'VALOR' in str(pieces.iloc[0,-1]) or 'VALOR' in str(pieces.iloc[1,-1]):
        pieces = pieces.iloc[1: , :]
    pieces = pieces[pieces['DESCRIPCION'].str.strip()!=""]
    
    pieces_clean = pieces[pieces['PESO NETO'].notna()].copy()
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
        template_path="helpers/templates/lau_importacion/Lau Importacion V3.tabula-template.json")

    for idx, table in enumerate(tables_full):
        if table.empty:
            continue
        try:
            result_clean, result = clean_columns(table)
            data_pieces_clean.append(result_clean)
            data_pieces.append(result)
        except:
            # raise(f"error cannot extract page {idx+1}")
            pass

    pieces_clean = pd.concat(data_pieces_clean).reset_index(drop=True)
    pieces = pd.concat(data_pieces)  
    return pieces_clean, pieces

def extract_data_mmj_import(filename):
    pieces_clean, pieces = extract_from_pdf(filename)
    if str(pieces.iloc[-1,1]) == 'KGS':
        pieces = pieces.iloc[:-2,:]
        pieces_clean = pieces_clean.iloc[:-2,:] 
    else:
        pieces = pieces.iloc[:-1,:]
        pieces_clean = pieces_clean.iloc[:-1,:] 
    # print(pieces)
    # print(pieces_clean)
    pieces_clean = separate_description(pieces_clean)
    pieces_clean = extract_pieces_data(pieces, pieces_clean)    
    print(type(pieces_clean))
    return pieces_clean


