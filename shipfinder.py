import tools.RelugarExpretions as RelugarExpretions 
import glob
import tools.ScanPDFChecker as ScanPDFChecker
import tools.PdfReader as PdfReader


def ship_finder(word):
    if RelugarExpretions.serchCustomWord(word, "ship"):
        
        return word
def main():
    path = glob.glob('facturas/**/*.pdf')
    for file in path:
        if ScanPDFChecker.ispdfa(file):
            textPDF=PdfReader.reader(file)
            wordlistr=textPDF.split()
            for idx, i in enumerate(wordlistr):
                if ship_finder(i):
                    shipto=wordlistr[idx+2]+" "+wordlistr[idx+3]+" "+wordlistr[idx+4]
                    print(shipto)
            
              
if __name__ == "__main__":
    main()