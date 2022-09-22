from ast import parse
import tabula
import pandas as pd
import re
import numpy as np
from db_custom import insert_item,getlastidInvoices
# pd.options.display.max_columns = None
# pd.options.display.max_rows = None
def create_column_name(parts):
    name = ''
    for part in parts:
        part = str(part)
        if 'nan' in part or 'Unnamed' in part:
            continue
        name += part
    return name

def separate_brutos_netos(pieces_clean):
    new = pieces_clean['brutos y netos'].str.split(n=2, expand=True)
    pieces_clean['brutos'] = new[0]
    pieces_clean['netos'] = new[1]
    del pieces_clean['brutos y netos']
    return pieces_clean

def separate_materia_prima(pieces_clean):
    if 'materia prima y agregado' not in pieces_clean.columns:
        return pieces_clean
    new = pieces_clean['materia prima y agregado'].str.replace('$', '', regex=False).str.split(n=2, expand=True)
    pieces_clean['materia prima'] = new[0]
    pieces_clean['agregado'] = new[1]
    del pieces_clean['materia prima y agregado']
    return pieces_clean

def extract_origin(pieces):
    pieces_new = pieces[pieces['brutos y netos'].isna()]
    try:
        extract_one = pieces_new['umc'].fillna('')
        extract_one = extract_one[extract_one.str.contains("origen")]
        parts = extract_one.str.rsplit(expand=True, n=1)
        return parts[1].to_list()
    except:
        extract_two = pieces_new['descripcion'].fillna('')
        extract_two = extract_two[extract_two.str.contains("Hecho en")]
        parts = extract_two.str.rsplit('Fraccion', expand=True, n=1)
        subparts = parts[0].str.rsplit(expand=True, n=1)
        return subparts[1].to_list()

# Clean columns
def clean_columns(pieces):
    pieces = pieces.dropna(how='all', axis=1)
    
    old_columns = ['' if 'Unnamed' in x else x for x in pieces.columns[:].tolist()]
    new_columns = [create_column_name(x) for x in zip(old_columns,pieces.iloc[0,:],pieces.iloc[1,:])]
    if 'DESCRIPCION DE LA MERCANCIA' not in new_columns:
        raise Exception("Cannot clean header")
    description_idx = new_columns.index('DESCRIPCION DE LA MERCANCIA')
    
    new_columns[-2] = 'td6'
    new_columns[-3] = 'td5'
    new_columns[-4] = 'td4'
    new_columns[0] = 'brutos y netos'
    new_columns[1] = 'cantidad'
    new_columns[2] = 'umc'
    new_columns[description_idx] = 'descripcion'
    new_columns[description_idx+1] = 'td1'
    new_columns[description_idx+2] = 'cantidad y clase'
    new_columns[description_idx+3] = 'td2'
    new_columns[description_idx+4] = 'materia prima y agregado'
    new_columns[description_idx+5] = 'td3'
    new_columns[-1] = 'total'

    if description_idx == 4:
        new_columns[3] = 'td0'
    
    pieces.columns = new_columns
    pieces = pieces.iloc[2: , :]
    pieces_clean = pieces[pieces['brutos y netos'].notna()].copy()
    umc_separate = pieces_clean['umc'].str.split(n=1, expand=True)
    try:
        pieces_clean.loc[:,'umc'] = umc_separate[0]
        pieces_clean.loc[:,'descripcion'] = umc_separate[1]
    except Exception:
        pass
    if 'td0' in pieces_clean.columns:
        pieces_clean['td0'].fillna('', inplace=True)
        pieces_clean['descripcion'].fillna('', inplace=True)
        pieces_clean["descripcion"] = pieces_clean["td0"].astype(str) + pieces_clean["descripcion"]
        del pieces_clean['td0']
    pieces_clean = pieces_clean[pieces_clean['descripcion'].notna()]
    pieces_clean = pieces_clean[pieces_clean['descripcion'] != 'Totales']
    pieces_clean = pieces_clean.dropna(how='all', axis=1)
    try:
        pieces_clean['cantidad y clase'] = pieces_clean['cantidad y clase'].str.replace('$', '', regex=False)
    except Exception:
        pass
    
    if 'td1' in pieces_clean.columns:
        pieces_clean['td1'].fillna('', inplace=True)
        pieces_clean['cantidad y clase'].fillna('', inplace=True)
        pieces_clean["cantidad y clase"] = pieces_clean["td1"].astype(str) + pieces_clean["cantidad y clase"]
        del pieces_clean['td1']

    if 'td2' in pieces_clean.columns:
        if 'materia prima y agregado' in pieces_clean.columns:
            pieces_clean["materia prima y agregado"] = pieces_clean["materia prima y agregado"] + pieces_clean["td2"].astype(str) 
        else:
            pieces_clean["materia prima y agregado"] = pieces_clean["td2"].astype(str)

        del pieces_clean['td2']   
    for i in range(1,7):
        if f'td{i}' in pieces_clean.columns:
            pieces_clean["materia prima y agregado"] = pieces_clean["materia prima y agregado"]  + pieces_clean[f"td{i}"].astype(str)
            del pieces_clean[f'td{i}']

    try:
        parts = pieces_clean['total'].str.rstrip(n=1, expand=True)
        pieces_clean['total'] = parts[1]
        pieces_clean['materia prima y agregado'] = pieces_clean['materia prima y agregado'] + parts[0]
    except Exception:
        pass

    return pieces_clean, pieces

def extract_from_pdf(filename):
    data_pieces_clean = [pd.DataFrame()]
    data_pieces = [pd.DataFrame()]
    tables_full = tabula.read_pdf_with_template(input_path=filename,
        template_path="helpers/templates/jabil_exportacion/Jabil Exportacion P1.tabula-template.json")

    tables_middle = tabula.read_pdf_with_template(input_path=filename,
        template_path="helpers/templates/jabil_exportacion/Jabil Exportacion PL.tabula-template.json")

    for idx, table in enumerate(tables_full):
        try:
            result_clean, result = clean_columns(table)
            data_pieces_clean.append(result_clean)
            data_pieces.append(result)
        except:
            if len(tables_middle[idx].index) < 3:
                print(f"page ommited: {idx+1}")
                continue
            try:
                result_clean, result = clean_columns(tables_middle[idx])
                data_pieces_clean.append(result_clean)
                data_pieces.append(result)
            except:
                print(f"page ommited: {idx+1}")
                continue


    pieces_clean = pd.concat(data_pieces_clean)
    pieces = pd.concat(data_pieces)  
    return pieces_clean, pieces

def extract_data_mmj_export(filename):
    pieces_clean, pieces = extract_from_pdf(filename)
    pieces_clean = pieces_clean[pieces_clean['cantidad'].notna()].copy()
    pieces_clean = separate_brutos_netos(pieces_clean)
    pieces_clean = separate_materia_prima(pieces_clean)
    total=(pieces_clean['total'].str.replace(',','').astype(float).sum())

    costperunit = total/float(pieces_clean['cantidad'].iloc[0])
    
    #give format to the data
    costperunit = "{:.2f}".format(costperunit)
    costperunit = total/float(pieces_clean['cantidad'].iloc[0])

    costperunit = "{:.2f}".format(costperunit)
    for index,row in pieces_clean.iterrows():
        print(row['cantidad'])
        print(row['umc'])
        print(row['descripcion'])
        print(row['total'])
        insert_item(Quantity_items=str(row['cantidad']),Mesure_items=str(row['umc']),Description_items=str(row['descripcion']),Cost_items=costperunit)
  


