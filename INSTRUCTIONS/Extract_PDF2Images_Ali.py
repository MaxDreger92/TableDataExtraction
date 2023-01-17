import fitz
import os
import shutil
from io import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from PyPDF2 import PdfFileReader, PdfFileWriter


def get_info(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        
    #author = info.author
    #creator = info.creator
    #producer = info.producer
    #subject = info.subject
    #title = info.title
    print (info.author)
    return info.author

#function that will use PyMuPDF (fitz) to extract images from PDF
def get_pics_from_pdf(doc):
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            width = img[2]
            height = img[3]
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha < 4:   # this is GRAY or RGB; can be saved as PNG
                pix.writePNG("img%s-%s_%sx%s.png" % (i, xref, width, height))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("img%s-%s_%sx%s.png" % (i, xref, width, height))
                pix1 = None   # free Pixmap resources
            pix = None        # free Pixmap resources
    return pix1

def extract_images_from_PDF(pdfName):
    directoryName = pdfName[:-4] + '_IMAGES'
    
    if os.path.isdir(directoryName):
        try:
            #os.rmdir(directoryName)
            shutil.rmtree(directoryName)
        except OSError:
            print ("Unable to remove folder: %s" % directoryName)
    else:
        try:
            if os.path.exists(directoryName):
                shutil.rmtree(directoryName)
        except OSError:
            print ("Unable to remove file: %s" % directoryName)
    os.makedirs(directoryName) #Directory where jpgs will be extracted
    currentDirectory = os.getcwd() #Gets the current directory
        
    path = os.path.join(currentDirectory,directoryName)
    shutil.copy(pdfName, path)
    os.chdir(path) #Change to the images folder
    #os.system("pdfimages "+ pdfName+" image -png")
    doc = fitz.open(pdfName)
# For documentation see
# https://pymupdf.readthedocs.io/en/latest/document/
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            width = img[2]
            height = img[3]
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha < 4:   # this is GRAY or RGB; can be saved as PNG
                pix.writePNG("img%s-%s_%sx%s.png" % (i, xref, width, height))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("img%s-%s_%sx%s.png" % (i, xref, width, height))
                pix1 = None   # free Pixmap resources
            pix = None        # free Pixmap resources
    
    #print(extract_pdf_info(pdfName))
    get_info(pdfName)
    pdf = PdfFileReader(open(pdfName, 'rb'))
    
    
    Author= pdf.getDocumentInfo().get("/Author","")
    Title= pdf.getDocumentInfo().get("/Title","")
    Subject=pdf.getDocumentInfo().get("/Subject","")
    print(Author)
     
    #print (pdf.getDocumentInfo())
    with open(pdfName[:-4]+'_REF.txt', 'w') as my_ref_file:  
        my_ref_file.write('Author='+Author+'\n')
        my_ref_file.write("Title=" +Title+',\n')
        my_ref_file.write("Subject="+ Subject+',\n')
    
    
    print ("Author:", pdf.getDocumentInfo().get("/Author",""))
    print ("Title:", pdf.getDocumentInfo().get("/Title",""))
    print ("Subject:", pdf.getDocumentInfo().get("/Subject",""))
    
#     with open('Dataset_'+pdfName[:-4]+'.txt', 'w') as my_ref_file:  
#         my_ref_file.write('EC:                           \n')
#         my_ref_file.write('Electrolyte:                    \n')
#         my_ref_file.write('PH:                            \n')
#         my_ref_file.write('Applied Potential:                   \n')
#         my_ref_file.write('Work Function, Phi:                   \n')
#         my_ref_file.write('Fermi Energy, E_f :                   \n')
        
#         my_ref_file.write('Adsorption Energy site:                   \n')
#         my_ref_file.write('Methodology:                   \n')
#         my_ref_file.write('EX Functional:                   \n')
        
#         my_ref_file.write('Packages:                   \n')
    with open(pdfName[:-4]+'.txt', 'w') as my_ref_file:
        my_ref_file.write('                           \n')
    #print (os.getcwd())
    os.chdir('..')
    return 

path=os.getcwd()
pdf_files = [f for f in os.listdir(path) if f.endswith('.pdf')]
#get_pics_from_pdf("test.pdf")


for files in pdf_files:
    print(files)
   # get_pics_from_pdf(files)
    extract_images_from_PDF(files)