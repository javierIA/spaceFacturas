import tabula
import pandas as pd
import re
import numpy as np
from helpers.tools.table_utils import umc_values, get_num_pages, index_containing_substring


def use_template_page_one(filename):
    tables_body = tabula.read_pdf_with_template(input_path=filename,
        template_path="helpers/templates/tegrant/TegrantP1.tabula-template.json")

    alternate_templates = ['TegrantP1V.tabula-template.json', 'TegrantP1V2.tabula-template.json', 'TegrantP1V3.tabula-template.json']

    for template in alternate_templates:
        if any(['PATENTE' in x for x in tables_body[0].columns.to_list()]) or not 'DESCRIPCION MERCANCIA/Merchandise Description' in tables_body[0].columns.to_list():
            tables_body = tabula.read_pdf_with_template(input_path=filename,
                template_path=f"helpers/templates/tegrant/{template}")
       
    return tables_body

def create_column_name(parts):
    name = ''
    for part in parts:
        part = str(part)
        if 'nan' in part or 'Unnamed' in part:
            continue
        name += part
    return name

# Clean columns
def clean_columns(pieces):
    pieces_clean = pieces
    return pieces_clean, pieces

def extract_from_pdf(filename):
    data_pieces_clean = [pd.DataFrame()]
    data_pieces = [pd.DataFrame()]
    tables_full = tabula.read_pdf(filename, pages='all', stream=False, lattice=True)

    for idx, table in enumerate(tables_full):
        if 'FECHA PAGO' in table.columns:
            result_clean, result = clean_columns(table)
            data_pieces_clean.append(result_clean)
            data_pieces.append(result)

    pieces_clean = pd.concat(data_pieces_clean)
    pieces = pd.concat(data_pieces)  
    return pieces_clean, pieces

def extract_data_estapack_iduspac(filename):
    pieces_clean, pieces = extract_from_pdf(filename)
    return pieces_clean

# filename = 'facturas/jabil_exportacion/17.pdf'
# result = extract_data(filename)
# print(result)


