import tabula
import pandas as pd
import re
import numpy as np
from helpers.tools.table_utils import umc_values, get_num_pages

def create_column_name(parts):
    name = ''
    for part in parts:
        part = str(part)
        if 'nan' in part or 'Unnamed' in part:
            continue
        name += f' {part}'
    return name.strip()

# Clean columns
def clean_columns(pieces):
    pieces_clean = pieces[pieces['PRODUCT NO.'].notna()].copy()

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

def extract_data_estapack_pcm(filename):
    pieces_clean, pieces = extract_from_pdf(filename)
    print
    return pieces_clean

# filename = 'facturas/jabil_importacion/8.pdf'
# result = extract_data(filename)
# print(result)
