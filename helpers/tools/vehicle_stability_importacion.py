import tabula
from PyPDF2 import PdfFileReader
import pandas as pd
from helpers.tools.table_utils import *
from db_custom import insert_item
def get_num_pages(filename):
    reader = PdfFileReader(filename)
    return reader.numPages

def only_numerics(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))

# Extract info from page 1 ---------------
# information = {}
# # Extract header
# table_header = tabula.read_pdf_with_template(input_path="facturas/ptv/PTV6.pdf",
#     template_path="templates/ptv/PTV Header.tabula-template.json")

# information['factura'] = table_header[0].iloc[0]['FACTURA']
# information['seccion aduana'] = table_header[0].iloc[0]['ADUANA-SECCION']
# information['pedimiento'] = table_header[0].iloc[0]['PEDIMENTO']

# Clean columns
def clean_columns(pieces):
    old_columns = ['' if 'Unnamed' in x else x for x in pieces.columns[:].tolist()]
    new_columns = [str(x[0])+str(x[1]) for x in zip(old_columns,pieces.iloc[0,:])]
    pieces.columns = new_columns
    pieces = pieces.iloc[1: , :]
    pieces_clean = pieces[pieces['DESCRIPCION'].notna()].copy()
    pieces_clean = pieces_clean[pieces_clean['PDA PARTE'].notna()]
    del pieces_clean['nan']
    return pieces_clean, pieces


# Get pieces origin
def extract_origin(pieces):
    pieces_origin = pieces[pieces['DESCRIPCION'].isna()]
    pieces_origin = pieces_origin[pieces_origin['PDA PARTE'].str.contains("Origen")]['PDA PARTE'].to_list()
    pieces_origin = [x.split(" ")[1] for x in pieces_origin]

    return pieces_origin

# Get additional info
def extract_additional_info(pieces):
    additional_info = pieces[pieces['DESCRIPCION'].isna()]
    additional_info = additional_info[additional_info['PDA PARTE'].str.contains("MARCA")]['PDA PARTE'].to_list()

    return additional_info

#Separate PDA Parte
def get_pda(pieces_clean):
    return [x.split(' ')[1] if len(x.split(' ')[0]) > len(x.split(' ')[1]) else x.split(' ')[0]  for x in pieces_clean['PDA PARTE'].to_list()]

def get_part(pieces_clean):
    return [x.split(' ')[0] if len(x.split(' ')[0]) > len(x.split(' ')[1]) else x.split(' ')[1] for x in pieces_clean['PDA PARTE'].to_list()]

def clean_pda_parte_column(x):
    parts = x.split()
    parts_cleaned = [only_numerics(part) for part in parts]
    new_value = " ".join(parts_cleaned)
    return new_value.strip()

def clean_pda_parte(pieces_clean):
    pieces_clean['PDA PARTE'] = pieces_clean['PDA PARTE'].apply(lambda x: clean_pda_parte_column(x))
    pieces_clean['PDA'] = get_pda(pieces_clean)
    pieces_clean['PARTE'] = get_part(pieces_clean)
    del pieces_clean['PDA PARTE']
    pieces_clean = pieces_clean.reset_index(drop=True)
    return pieces_clean

def extract_data_vehicle_stability_import(filename):
    template_one="helpers/templates/ptv/PTV BodyP1.tabula-template.json"
    template_n="helpers/templates/ptv/PTV BodyPM.tabula-template.json"
    pieces_clean, pieces = extract_from_pdf(
        filename,
        template_one,
        template_n,
        clean_columns
    )
    pieces_clean['ORIGEN'] = extract_origin(pieces)
    pieces_clean['ADDITIONAL_INFO'] = extract_additional_info(pieces)
    pieces_clean = clean_pda_parte(pieces_clean)
    pieces_clean = pieces_clean.reset_index(drop=True)
    for index,row in pieces_clean.iterrows():
        CANTIDAD,UM = row['CANTIDAD UM'].split(' ')
        #romove $ row['PRECIO UNITARIO']
        unit= row['UNITARIO'].replace('$','')
        unit= unit.replace(',','')
        unit= float(unit)
        insert_item(Description_items=row['DESCRIPCION'],Quantity_items=float(CANTIDAD),Mesure_items=UM,Cost_items=unit)
    return pieces_clean

# filename = 'facturas/vehicle_stability_importacion/3.pdf'
# result = extract_data(filename)
# print(result)
