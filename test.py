import datetime
from tools import PdfTools
import db as db
import utils as utils
from helpers import selector
from pathlib import Path
from db_custom import getlastidInvoices, insert_invoice,insert_item, multiplyItems
from datetime import date
import logging
import ia 
import tools.RelugarExpretions as RelugarExpretions
pdfs=db. get_pdfs()
arrayimport=['import','imports','importacion','importación','IMPORT','IMPORTS','I M P O R T A C I O N','IMPORTACIÓN','I  M  P  O  R  T  A  C  I  O  N']
arrayexport=['export','exports','exportacion','exportación','EXPORT','EXPORTS','E X P O R T A C I O N','EXPORTACIÓN','E  X  P  O  R  T  A  C  I  O  N']


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

def extract_words(text,word):
    wordlist=map(lambda x: utils.word_finder(x,word) ,text.split())
    wordlist=list(filter(None,wordlist))
    wordlist=list(set(wordlist))
    return wordslist
def extract_type(text):
    typepdf=""
    for matcher in arrayimport:
       if utils.validte_words(matcher,text):
            typepdf="import"
    for matcher in arrayexport:
        if utils.validte_words(matcher,text):
            typepdf="export"
    if typepdf=="":
        typepdf="other"
    
    return typepdf

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.disable(logging.INFO)

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
                    #romove duplicate elements
                    rfclist=list(set(rfclist))
                    print(rfclist)
                    logging.error(typepdf+ " - " +str(pdf.path_pdfs))
                    for rfc in rfclist:
                        if rfc!="SICO5407099U2" and rfc!="IACL5612133X0" and  rfc!="SICA660112JJ4":
                            
                            if not db.get_client(rfc):
                                print("No existe el cliente")
                                pass
                            if not datelist:
                                date=date.today()
                            else:
                                date=datelist[0]
                            insert_invoice(RFC_clients=rfc,Date_invoices=date,Total_invoives=0,Origin_invoices=getName(rfc))  
                            selector.selectorTemplate(RFC=rfc,TYPE=typepdf,PATH=path_pdfs)
                            multiplyItems(getlastidInvoices())
                            update_status(id_pdfs,"processed")
                            break
                            pass
                    
                else:   
                    ia.extract_type(path_pdfs,textPDF)
                    update_status(id_pdfs,"processed")
            except Exception as e:
                logging.error(e)
                print(e)    
                status_pdfs="error"
                logging.error(pdf.path_pdfs)
                update_status(id_pdfs,status_pdfs)
                continue      
            
                
                
            
