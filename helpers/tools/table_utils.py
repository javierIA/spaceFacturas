from PyPDF2 import PdfFileReader
import tabula
import pandas as pd

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