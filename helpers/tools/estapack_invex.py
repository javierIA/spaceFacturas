import tabula
import pandas as pd
import re
import numpy as np
from helpers.tools.table_utils import umc_values, get_num_pages, index_containing_substring
from db_custom import insert_item
def separate_price_unit(pieces_clean):
    pieces_clean['PRICE / UNIT'] = pieces_clean['PRICE / UNIT'].str.replace('/', '', regex=False)
    pieces_clean['PRICE / UNIT'] = pieces_clean['PRICE / UNIT'].str.replace('$', '', regex=False)

    parts = pieces_clean['PRICE / UNIT'].str.split(expand=True, n=2)
    pieces_clean['PRICE'] = parts[0]
    pieces_clean['UNIT'] = parts[1]
    del pieces_clean['PRICE / UNIT']
    return pieces_clean



def extract_order_number(pieces):
    pieces_new = pieces[pieces['PRODUCT NO.'].isna()]
    pieces_new = pieces_new[pieces_new['DESCRIPTION'].str.contains("Order No.")]['DESCRIPTION'].to_list()
    pieces_new = [x.split()[-1] for x in pieces_new]

    return pieces_new

def clean_qty_columns(pieces_columns):
    pieces_columns['QTY. ORDERED'] = pieces_columns["QTY. ORD'D"].str.rsplit(expand=True, n=2)[0]
    del pieces_columns["QTY. ORD'D"]
    pieces_columns['QTY. SHIPPED'] = pieces_columns['QTY. SHIPPED'].str.rsplit(expand=True, n=2)[0]

    return pieces_columns

# Clean columns
def clean_columns(pieces):
    pieces_clean = pieces[pieces['PRODUCT NO.'].notna()].copy()
    if 'Unnamed: 0' in pieces_clean.columns and 'B/O' in pieces_clean.columns:
        pieces_clean['B/O'].fillna(pieces_clean['Unnamed: 0'], inplace=True)
        del pieces_clean['Unnamed: 0']

    if 'AMOUNT' in pieces_clean.columns:
        pieces_clean['AMOUNT'] = pieces_clean['AMOUNT'].str.replace('$', '', regex=False)

    return pieces_clean, pieces

def extract_from_pdf(filename):
    data_pieces_clean = [pd.DataFrame()]
    data_pieces = [pd.DataFrame()]
    tables_full = tabula.read_pdf_with_template(input_path=filename,
        template_path="helpers/templates/estapack_invex/Estapack-invex.tabula-template.json")

    for idx, table in enumerate(tables_full):
        try:
            result_clean, result = clean_columns(table)
            data_pieces_clean.append(result_clean)
            data_pieces.append(result)
        except:
            raise("error cannot extract")

    pieces_clean = pd.concat(data_pieces_clean)
    pieces = pd.concat(data_pieces)  
    return pieces_clean, pieces

def extract_data_estapack_invex(filename):
    pieces_clean, pieces = extract_from_pdf(filename)
    pieces_clean['ORDER NO'] = extract_order_number(pieces)
    pieces_clean = separate_price_unit(pieces_clean)
    pieces_clean = clean_qty_columns(pieces_clean)
    for index, row in pieces_clean.iterrows():
        insert_item(Description_items=row['DESCRIPTION'], Quantity_items=row['QTY. ORDERED'], Mesure_items=row['UNIT'], Cost_items=row['PRICE'])
    return pieces_clean

# filename = 'facturas/estapack_invex/8.pdf'
# result = extract_data(filename)
# print(result)
# print(result.columns)

