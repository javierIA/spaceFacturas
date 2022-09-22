
from modulefinder import IMPORT_NAME
from os import EX_CANTCREAT
from unicodedata import name
import tools.RelugarExpretions as RelugarExpretions 
import glob 
import tools.PdfTools as PdfTools
import db as db 
from helpers import selector

def validate_rfc(word):
    if RelugarExpretions.validRFC(word):
        return word
def validate_date(word):
    if RelugarExpretions.validDate(word):
        return word
def db_select(word):
    return db.get_client(word)
def validte_words(word,words):
    for importword in words:
        if RelugarExpretions.searchCustomWord(word, importword):
            return word
 
def word_finder(word,matcher):
    if RelugarExpretions.searchCustomWord(word, matcher):
        return word       

def main():
    arrayimport=['import','imports','importacion','importación']
    arrayexport=['export','exports','exportacion','exportación']

    path = glob.glob('facturas/**/*.pdf')
    for file in path:
        if PdfTools.ispdfa(file):
            typepdf=""
            textPDF=PdfTools.reader(file)
            wordlistr=textPDF.split()   
            for word in wordlistr:   
                for matcher in arrayimport:
                    if validte_words(word,matcher):
                        typepdf="import"
                        
                        
                for matcher in arrayexport:
                    if validte_words(word,matcher):
                        typepdf="export"
            if typepdf=="":
                typepdf="other"
            rfclist=map(validate_rfc ,textPDF.split())
            rfclist=list(filter(None,rfclist))
            rfclist=list(set(rfclist))
            datelist=map(validate_date ,textPDF.split())
            datelist=list(filter(None,datelist))
            datelist=list(set(datelist))
            if not rfclist:
                f=open("notRFCList.txt", "a+")
                f.write(file+"\n")
            else:
                f=open("RFCSend.txt", "a+")
                for rfc in rfclist:
                    if db_select(rfc):
                        client=db_select(rfc)
                        selector(client,typepdf,file)
                    else:
                        print(rfc)
            print(file,rfclist,datelist)




if __name__ == "__main__":
    main()