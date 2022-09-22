from tools import PdfTools
import db as db
import utils as utils
from helpers import selector
from pathlib import Path
from db_custom import insert_invoice,insert_item
from datetime import date
pdfs=db. get_pdfs()
arrayimport=['import','imports','importacion','importación']
arrayexport=['export','exports','exportacion','exportación']


def update_status(pdf,status):
    db.update_pdf(pdf,status)
def extract_rfc(text):
    rfclist=map(utils.validate_rfc ,text.split())
    rfclist=list(filter(None,rfclist))
    rfclist=list(set(rfclist))
    return rfclist
def extract_date(text):
    datelist=map(utils.validate_date ,text.split())
    datelist=list(filter(None,datelist))
    datelist=list(set(datelist))
    return datelist
def getName(rfc):
    client=db.get_client(rfc)
    if client is None:
        return "No existe el cliente"
    else:
        return client.Name_clients


def extract_type(text):
    typepdf=""
    wordlistr=text.split()   
    for word in wordlistr:   
        for matcher in arrayimport:
            if utils.validte_words(word,matcher):
                typepdf="import"
        for matcher in arrayexport:
            if utils.validte_words(word,matcher):
                typepdf="export"
    if typepdf=="":
        typepdf="other"
    return typepdf

for pdf in pdfs:
    id_pdfs=pdf.id_pdfs
    author_pdfs=pdf.author_pdfs
    path_pdfs=pdf.path_pdfs
    status_pdfs=pdf.status_pdfs 
    path_pdfs=Path(path_pdfs)
    if pdf.status_pdfs=="pending":
        if PdfTools.ispdfa(path_pdfs):
            textPDF=PdfTools.reader(path_pdfs)
            rfclist=extract_rfc(textPDF)
            datelist=extract_date(textPDF)
            typepdf=extract_type(textPDF)
            try:
                if len(rfclist)>0:
                    for rfc in rfclist:
                        if rfc!="SICO5407099U2":
                            print(rfc)
                            if not datelist:
                                date=date.today()
                            else:
                                date=datelist[0]
                            print(getName(rfc))
                            insert_invoice(RFC_clients=rfc,Date_invoices=date,Total_invoives=0,Origin_invoices=getName(rfc))    
                            selector.selectorTemplate(RFC=rfc,TYPE=typepdf,PATH=path_pdfs)
    
                            #update_status(id_pdfs,status_pdfs="processed")
                else:
                    status_pdfs="IA"
                    update_status(id_pdfs,status_pdfs)
            except Exception as e:
                print(e)
                status_pdfs="error"
                update_status(id_pdfs,status_pdfs)
                continue      
            
                
                
            
    