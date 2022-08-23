import glob
from io import StringIO
from itertools import count
import tools.ScanPDFChecker as ScanPDFChecker
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import spacy_transformers
import spacy
import tools.PdfReader as PdfReader
import tools.ScanPDFChecker as ScanPDFChecker
def main():
    path=open("notRFC.txt", "r")
    paths=path.readlines()
 
    nlp_ner_model = spacy.load('model-best')
    for file in paths:
        file=file.replace("\n","")
        if ScanPDFChecker.ispdfa(file):
            textPDF=PdfReader.reader(file)
            doc = nlp_ner_model(textPDF)
            f=open("taxID.txt", "a+")
            print(doc.ents)
            f.write(str(doc.ents)+"\n")
              
    
    None
    
def count_files():    
    path = glob.glob('facturas/**/*.pdf')
    print(len(path))
    
if __name__ == "__main__":
    main()
   