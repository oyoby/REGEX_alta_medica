from utils import *
import os
import PyPDF4
import pandas as pd
import re

errors_list = []
count = 0
directory = 'C:/Users/andre/Desktop/Prescotts_project/Data'
all_users_df = pd.DataFrame()

for folder in os.listdir(directory):
    #print(folder)
    for file in os.listdir(str(directory + '/' + folder)):
        try:
            print(file)
            user_dict = doc_dict
            filepath = str(directory + '/' + folder + '/' + file)
            pdfFileObj = open(filepath, 'rb')
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
            pageObj = pdfReader.getPage(0)
            pageText = pageObj.extractText()
            pageText_no_breaks = re.sub(r'\n', '', pageText).lower()

            print(pageText_no_breaks)
            #Useful expressions
            Name = re.search(r'nome:nº proc\. clínico: \d* (.*)data de nascimento:', pageText_no_breaks).group(1)
            procNum = re.search(r'nome:nº proc\. clínico: (\d*) .*data de nascimento:', pageText_no_breaks).group(1)

            DataAltaClinica = re.search(r'alta clínica[^*]*?(\d\d-\d\d-\d\d\d\d)', pageText_no_breaks).group(1)


            #add to dict
            user_dict['Nome'] = [Name]
            user_dict['Nº Processo'] = [procNum]
            user_dict['DataAltaClinica'] = [DataAltaClinica]

            Diagnósticos = re.search(r'Diagnósticos:', pageText_no_breaks)
            if Diagnósticos:
                print('Diagnósticos')
                Diagnósticos_text = re.search( r'Diagnósticos:(.*)Motivo de Internamento:' , pageText_no_breaks).group(1)
                Diagnósticos_text = re.sub(r'- ', '\n- ', Diagnósticos_text)
                #print(Diagnósticos_text)
        except:
            user_dict = { 'Nome' : [filepath], 'Nº Processo' : ['erro'], 'DataAltaClinica' : ['erro'] }
            errors_list.append(filepath)


        user_df = pd.DataFrame.from_dict(user_dict)
        all_users_df = all_users_df.append(user_df)
        
all_users_df.to_excel(r'C:\Users\andre\Desktop\Prescotts_project\Output\output.xlsx')

