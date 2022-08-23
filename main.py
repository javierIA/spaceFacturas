
import tools.RelugarExpretions as RelugarExpretions 
import tools.ScanPDFChecker as ScanPDFCheck
import glob 
import tools.PdfReader as PdfReader
def validate_rfc(word):
    if RelugarExpretions.validRFC(word):
        return word
def validate_date(word):
    if RelugarExpretions.validDate(word):
        return word

def main():
    path = glob.glob('facturas/**/*.pdf')
    for file in path:
        if ScanPDFCheck.ispdfa(file):
            textPDF=PdfReader.reader(file)
            rfclist=map(validate_rfc ,textPDF.split())
            rfclist=list(filter(None,rfclist))
            rfclist=list(set(rfclist))
            datelist=map(validate_date ,textPDF.split())
            datelist=list(filter(None,datelist))
            datelist=list(set(datelist))
            if not rfclist:
                f=open("notRFC.txt", "a+")
                f.write(file+"\n")
            print(file,rfclist,datelist)




if __name__ == "__main__":
    main()