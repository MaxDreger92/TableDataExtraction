# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 13:26:10 2020

@author: alimalek
"""
# =============================================================================
import glob, os, shutil

path = os.getcwd()
target = "C:\\Users\\alima\\OneDrive\\Desktop\\Textfiles\\All_TXT_FILES"
# list all the directories in current directory
dirs=[ x for x in os.listdir('.') if os.path.isdir(x) ]

for d in dirs:
#    list all files in A/*, B/*, C/*...
     files_to_copy = os.listdir(os.path.join(d))  

     for f in files_to_copy:
          if f.endswith(".txt"):  ## copy the relevant files to dest
              shutil.copy(os.path.join(d, f), target)
#  =============================================================================


