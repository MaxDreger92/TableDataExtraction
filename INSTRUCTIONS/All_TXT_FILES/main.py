# Import Libraries

# Main Libraries
import pandas as pd
import numpy as np

# Other Important Libraries
import re; # regular expression
import os

from ExtractDataFromText import extractData

# List of all the files in the current folder and List of Parameters Name
def list_of_text_files_in_the_current_folder():
    ''' LIST OF ALL THE TXT FILES IN THE CURRENT FOLDER '''
    
    import os
    files = [f for f in os.listdir('.') if os.path.isfile(f)];

    text_file_list = [];
    for names in files:
        if names.endswith(".txt"):
            text_file_list.append(names)
    return text_file_list


def keywords_for_variables():
    """ Returns a list of keywords """
    
    filename= 'keywords.xlsx'
    keywords= list(pd.read_excel(filename))+['x','y', 'xvalue', 'yvalue']
    
    def get_keyword(function):
        ldict = {}
        exec(function,globals(),ldict)
        keyword = ldict['keyword']
        return keyword
    
    def keywords_function(keywords):
        ''' SETTING KEYWORDS FOR EAFCH ATTRIBUTES '''
        for i in range(len(keywords)):
            if (keywords[i]!= 'xvalue' and keywords[i]!='yvalue'):
                function= 'keyword='+'\"'+keywords[i]+'=(.*?),\"'
            elif keywords[i]== 'xvalue' :
                function= 'keyword='+'\"'+'(.*?),\"'
            else:
                function= 'keyword='+'\"'+',(.*?)\\n'+'\"'
            keywords[i]= get_keyword(function)
        return keywords

    keywords= keywords_function(keywords)
    return keywords


# List of TXT Files in the current folder
file_list= list_of_text_files_in_the_current_folder()

# Reading Keywords
keywords= keywords_for_variables()

DataFrame= extractData(file_list, keywords)

#Add refrences, Author, Title, Subject to files

j=0
k=0
z=0

for i in range (DataFrame.shape[0]):
    if (DataFrame['cat'].isnull().iloc[i]) & (~DataFrame['Author'].isnull().iloc[i]):
        Names1 = DataFrame['Author'][i]
        DataFrame['Author'][j:i] = Names1
        j=+i
    
    elif (DataFrame['cat'].isnull().iloc[i]) & (~DataFrame['Title'].isnull().iloc[i]):
        Names2 = DataFrame['Title'][i]
        DataFrame['Title'][k:i] = Names2
        k=+i
        
    elif (DataFrame['cat'].isnull().iloc[i]) & (~DataFrame['Subject'].isnull().iloc[i]):
        Names3 = DataFrame['Subject'][i]
        DataFrame['Subject'][z:i] = Names3
        z=+i
        
        
N_index = list(DataFrame[DataFrame['cat'].isnull()].index)
DataFrame = DataFrame.drop(N_index, axis=0)


DataFrame.to_csv('Final_result.csv',index=None,header=True)








