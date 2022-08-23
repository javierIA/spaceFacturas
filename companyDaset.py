import tools.PdfReader as PdfReader
import tools.RelugarExpretions as RelugarExpretions
import tools.ScanPDFChecker as ScanPDFChecker
import glob 
import os 
def main():
    
    path = glob.glob('facturas/**/*.pdf')
    for file in path:
        if ScanPDFChecker.ispdfa(file):
            textPDF=PdfReader.reader(file)
            #save the text in a file
            foldername=os.path.dirname(file)
            foldername=foldername.replace('facturas/','')
            f=open(foldername+'.txt','a+')
            f.write(textPDF+'???')
            print(foldername)
            
            
    if not os.path.exists('txt'):
        os.makedirs('txt')
        
if __name__ == "__main__":
    main()
   