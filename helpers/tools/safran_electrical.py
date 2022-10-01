import tabula
from PyPDF2 import PdfFileReader
import pandas as pd
from helpers.tools.table_utils import *
from db_custom import insert_item
def extract_data_safran(filename):
    data_pieces_clean = [pd.DataFrame()]
    data_pieces = [pd.DataFrame()]
    tables = tabula.read_pdf(filename, pages='all', guess=False, stream=True)
    #romove NaN Rows
    tables = tables[~tables.isna().all(axis=1)]
    for index,row in tables.iterrows():
        insert_item(row['DESCRIPCION DE LA MERCANCIA'],row['CANTIDAD'],row['UMC'],row['COSTO UNIT'])
    print(tables)