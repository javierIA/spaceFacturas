import os
import utils
from tools import PdfTools
def extract_type(path,text):
    rfc={"absia":   "AOM-210617-IC7","absia2":"14660055","asbaltos":"14660055","asbaltos2":"31-1537655","HUTCHINSON":"HSM-000316-H84","modine":"39-048200005","ssi":"SSC-840823-JT3"}
    from utils import RelugarExpretions
    for key in rfc:
        for matcher in rfc[key].split():
            wordlist=map(lambda x: utils.word_finder(x,matcher) ,text.split())
            wordlist=list(filter(None,wordlist))
            wordlist=list(set(wordlist))
            if len(wordlist)>0:
                if key=="absia" or key=="absia2":
                    return "absia"
                elif key=="asbaltos" or key=="asbaltos2":
                    return "asbaltos"
                elif key=="HUTCHINSON":
                    return "HUTCHINSON"
                elif key=="modine":
                    return "modine"
                elif key=="ssi":
                    return "ssi"
                else:
                    return "unknown"   
            
def main():
    path="C://Users//javie//OneDrive//Documentos//facturas//spaceFacturas//facturas//SISTEMAS Y SERVICIOS DE COMUNICACION SA DE CV"
    from glob import glob
    pdfs=glob(path+"//*.pdf")
    for pdf in pdfs:
        if PdfTools.ispdfa(pdf):
            text=PdfTools.reader(pdf)
            extract_type(pdf,text)  
main()