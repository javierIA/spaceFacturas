from cgitb import text
import glob

from requests import patch
import tools.PdfReader as PdfReader
import tools.ScanPDFChecker as ScanPDFChecker

def main():
    path=open("notRFC.txt", "r")
    paths=path.readlines()
    for file in paths:
        file=file.replace("\n","")
        if ScanPDFChecker.ispdfa(file):
            textPDF=PdfReader.reader(file)
            print(file,textPDF)
            f=open('dataset.txt','a+')
            f.write(textPDF+'???')
            f.close()
            
            
            
if __name__ == "__main__":
    main()
    