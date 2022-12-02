import os
import utils
import camelot
from helpers.tools import abisa,asfaltos,hutchinson,modine,ssc,table_utils
import db_custom
import datetime

def insert_items(Description_items,Quantity_items,Mesure_items,Cost_items):
    Num_invoice=db_custom.getlastidInvoices()
    #convert data to float
    Quantity_items=float(Quantity_items)
    Cost_items=float(Cost_items)
    
    
    db_custom.insert_item(Description_items,Quantity_items,Mesure_items,Cost_items,Num_invoice)
def extract_type(path,text):
    rfc={"absia":   "AOM-210617-IC7","absia2":"14660055","asbaltos":"14660055","asbaltos2":"31-1537655","HUTCHINSON":"HSM-000316-H84","modine":"39-048200005","ssi":"SSC-840823-JT3"}
    try:
        for key in rfc:
            for matcher in rfc[key].split():
                wordlist=map(lambda x: utils.word_finder(x,matcher) ,text.split())
                wordlist=list(filter(None,wordlist))
                wordlist=list(set(wordlist))
                if len(wordlist)>0:
                    if key=="absia" or key=="absia2":
                        abisa.getTables(path)
                        return "absia"
                    elif key=="asbaltos" or key=="asbaltos2":
                        asfaltos.getTables(path)
                        return "asbaltos"
                    elif key=="HUTCHINSON":
                        hutchinson.getTables(path)
                        return "HUTCHINSON"
                    elif key=="modine":
                        modine.getTables(path)
                        return "modine"
                    elif key=="ssi":
                        ssc.getTables(path)
                        return "ssi"
                    else:
                        table = camelot.read_pdf(path, pages='1-end')
                        #export to excel 
                        path=path.replace(".pdf",".xlsx")
                        for i in range(len(table)):
                            table[i] = table_utils.clean_table(table[i])
                            table[i].to_excel(path, sheet_name='number_{}'.format(i))
                            db_custom.insert_invoice(RFC_clients="IA",Date_invoices=datetime.today(),Total_invoives=0,Origin_invoices=path)

                        return "unknown"   
    except Exception as e:
        print(e)
        pass            
