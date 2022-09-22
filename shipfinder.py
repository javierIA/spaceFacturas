
from array import array
import tools.RelugarExpretions as RelugarExpretions 
import glob
import tools.PdfTools as PdfTools


def ship_finder(word,matcher):
    if RelugarExpretions.searchCustomWord(word, matcher):
        return word
def main():
    path = glob.glob('facturas/**/*.pdf')
    arrayimport=['import','imports','importacion','importación']
    arrayexport=['export','exports','exportacion','exportación']
    foundImport=0
    foundExport=0
    for file in path:
        if PdfTools.ispdfa(file):
            textPDF=PdfTools.reader(file)
            wordlistr=textPDF.split()
            for word in wordlistr:
               for matcher in arrayimport:
                   if ship_finder(word,matcher):
                       print(file)
                       print(word)
                       foundImport=foundImport+1
                       pass
               for matcher in arrayexport:
                    if ship_finder(word,matcher):
                        print(file)
                        print(word)
                        foundExport=foundExport+1
                        pass
    print('foundImport: '+str(foundImport))
    print('foundExport: '+str(foundExport))
if __name__ == "__main__":
    main()