#!/usr/bin/env python
# coding: utf-8
# import library

from PIL import Image
import os
import re
import shutil
from io import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from PyPDF2 import PdfFileReader, PdfFileWriter



# get infromation of article like, author, title ...


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


# get images from PDF


def extract_images_from_PDF(pdfName):
    directoryName = pdfName[:-4] + '_IMAGES'
    
    if os.path.isdir(directoryName):
        try:
            #os.rmdir(directoryName)
            shutil.rmtree(directoryName, ignore_errors=True)
        except OSError:
            print ("Unable to remove folder: %s" % directoryName)
    else:
        try:
            if os.path.exists(directoryName):
                shutil.rmtree(directoryName, ignore_errors=True)
        except OSError:
            print ("Unable to remove file: %s" % directoryName)
    os.makedirs(directoryName) #Directory where jpgs will be extracted
    currentDirectory = os.getcwd() #Gets the current directory
        
    path = os.path.join(currentDirectory,directoryName)
    shutil.copy(pdfName, path)
    os.chdir(path) #Change to the images folder
    os.system("pdfimages.exe -j "+ pdfName+" image ")
    
    Images = [f for f in os.listdir('.') if os.path.isfile(f)];

    for image in Images:
        if image.endswith(".ppm") or image.endswith(".pbm") or image.endswith(".pgm"):
            Image.open(image).save(image[:-4]+'.jpg')
            os.remove(image)

    
    get_info(pdfName)
    pdf = PdfFileReader(open(pdfName, 'rb'))
        
    Author= pdf.getDocumentInfo().get("/Author","")
    Title= pdf.getDocumentInfo().get("/Title","")
    Subject=pdf.getDocumentInfo().get("/Subject","")
        #print (pdf.getDocumentInfo())
    with open(pdfName[:-4]+'_REF.txt', 'w') as my_ref_file:  
        my_ref_file.write('Author='+Author+',\n')
        my_ref_file.write("Title=" +Title+',\n')
        my_ref_file.write("Subject="+ Subject+',\n')
    
    
    print ("Author:", pdf.getDocumentInfo().get("/Author",""))
    print ("Title:", pdf.getDocumentInfo().get("/Title",""))
    print ("Subject:", pdf.getDocumentInfo().get("/Subject",""))
    
    with open(pdfName[:-4]+'.txt', 'w') as my_ref_file:
        my_ref_file.write('                           \n')
    os.chdir('..')
    return 


# read the current path and list all pdf files in the current path
path=os.getcwd()
pdf_files = [f for f in os.listdir(path) if f.endswith('.pdf')]

# extarct images from PDFs and put in afolder with its name

for files in pdf_files:
    print(files)
   # get_pics_from_pdf(files)
    extract_images_from_PDF(files)





