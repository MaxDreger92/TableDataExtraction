# Main Libraries
import pandas as pd
import numpy as np

# Other Important Libraries
import re; # regular expression
import os


def extractData(file_list, keywords):

    def reading_main_and_reference_text_files_linebyline(text_file_name):
        ''' READING AND RETURING MAIN TEXT FILE AND CORRESPONDING REFERENCE TEXT FILE LINE-BY-LINE'''
    
        text_file=open(text_file_name, 'r').readlines()
        while '\n' in text_file: text_file.remove('\n')
        return text_file
    
    
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
    
    def text_data_extraction(text, keywords):
        ''' EXTRACTING MAIN INFORMATION '''
        import re;
    
        column_names=[];
        for i in range(len(keywords)):
            if (keywords[i]!= '(.*?),' and ',(.*?)' not in keywords[i]):
                column_names.append(keywords[i].replace('=(.*?),',''))
            elif(keywords[i]== '(.*?),'):
                column_names.append('xvalue')
            else:
                column_names.append('yvalue')
    
    
    
        df= pd.DataFrame(columns= column_names)
    
        for i in range(len(text)):
            df.loc[i] = 'NA';
            for j in range(len(keywords)):
                try:
                    temp = re.search(keywords[j], text[i]);
                    if (column_names[j]!='xvalue' and column_names[j]!='yvalue'):
                        df[column_names[j]][i] = temp.group().replace(column_names[j]+'=','');
                        df[column_names[j]][i] = df[column_names[j]][i].replace(',','');
                    elif(column_names[j]=='xvalue'):
                        df[column_names[j]][i] = temp.group().replace(',','');
                    elif(column_names[j]=='yvalue'):
                        df[column_names[j]][i] = temp.group().replace(',','');
                        df[column_names[j]][i] = df[column_names[j]][i].replace('\n','');
    
                except AttributeError:
                    df[column_names[j]][i] = "NA";
        return df
    
    
    
    def placing_x_and_y_axis_values_under_correct_attribute_name(df, text, keywords):
        ''' DETERMING THE AXIS NAMES FOR X AND Y, EXTRACTING AND THEN PUTTING THEM UNDER THE CORRECT ATTRIBUTE COLUMN'''
    
        columns= list(df)
        count= 0;
    
        columnNumberX=1000;
        columnNumberY=1000;
        k=0;
        for i in range(len(text)):# for every line in the text file
            if count==0:
                if df['x'][i]!='NA':
                    for j in range(len(columns)):
                        if df['x'][i].strip()==columns[j]:
                            columnNumberX= j
                        if df['y'][i].strip()==columns[j]:
                            columnNumberY= j
                    count=1;
    
            if count==1 and df['x'][i+1]=='NA' and i+1<len(text)-1:
                try:
                    df[columns[columnNumberX]][i]= df['xvalue'][i+1]
                    df[columns[columnNumberY]][i]= df['yvalue'][i+1]
                except:
                    pass
                try:
                    for m in range(len(columns)):
                        if columns[m]!=columns[columnNumberX] and columns[m]!=columns[columnNumberY]:
                            df[columns[m]][i]= df[columns[m]][i-k]
                    k=k+1
                except:
                    pass
    
            else:
                count=0
                k=0
    
        return df
    
    def df_clean(df):
        """ Clean DataFrame """
        
        df= df.drop(columns=['x','y','xvalue','yvalue'])
        df= df[df!= 'NA'];
        df= df.dropna(how= 'all').reset_index(drop=True)
        return df
    
    
    
    
    dataFrame= pd.DataFrame();

    for i in range(len(file_list)):
        
        text= reading_main_and_reference_text_files_linebyline(file_list[i])
        df= text_data_extraction(text, keywords)
        df= placing_x_and_y_axis_values_under_correct_attribute_name(df, text, keywords)
        df= df_clean(df)
        dataFrame= dataFrame.append(df)
    dataFrame= dataFrame.dropna(how='all').reset_index(drop=True)
    print(dataFrame)
    return dataFrame
    