##importing 
import pandas as pd
from io import StringIO
#import logging
import requests
import re

def get_cik_list(dataframe):
    #logging.info('Returning the cik')
    return dataframe['cik']

def remove_html_tags(text):
    #logging.info('Removing the html tags in the response')
    clean = re.compile('<.*?>')
    remove_non_breaking_space = re.compile('&nbsp')
    clean_txt = re.sub(clean, '', text)
    clean_txt = re.sub(remove_non_breaking_space, ' ', clean_txt)
    clean_txt = re.sub(r'\n|\t', ' ', clean_txt)
    clean_txt = re.sub(r'[&#]+[0-9]+', ' ', clean_txt)
    return clean_txt
    

def max_length(array):
    max=0
    match = ""
    for elem in array:
        if(len(elem) > max):
            max = len(elem)
            match = elem
    return match

    
def fill_dictionary():
    dict = { "uncertain" : 0,
		"unemploy" : 0,
		"risk" : 0,
		"believe" : 0,
		"anticipate" : 0,
		"fluctuate" : 0,
        "indefinite" : 0,
        "likelihood" : 0,
        "unlikely" : 0,
        "likely" : 0,
        "possible": 0,
        "predict" : 0,
        "recession" : 0,
        "pandemic" : 0 }
    return dict

def count_words(item_1a_section):
    counts= fill_dictionary()
    words = item_1a_section.split()
    for word in words:
        if('uncertain' in word.lower()):
            counts['uncertain'] +=1
        elif('unemploy' in word.lower()):
            counts['unemploy'] +=1
        elif('risk' in word.lower()):
            counts['risk'] +=1
        elif('believe' in word.lower()):
            counts['believe'] +=1
        elif('anticipate' in word.lower()):
            counts['anticipate'] +=1
        elif('fluctuate' in word.lower()):
            counts['fluctuate'] +=1
        elif('indefinite' in word.lower()):
            counts['indefinite'] +=1  
        elif('likelihood' in word.lower()):
            counts['likelihood'] +=1
        elif('unlikely' in word.lower()):
            counts['unlikely'] +=1
        elif('likely' in word.lower()):
            counts['likely'] +=1
        elif('possible' in word.lower()):
            counts['possible'] +=1
        elif('predict' in word.lower()):
            counts['predict'] +=1
        elif('recession' in word.lower()):
            counts['recession'] +=1  
        elif('pandemic' in word.lower()):
            counts['pandemic'] +=1  
    return counts
    

#logging.basicConfig(filename='log_file.log',level=logging.DEBUG)

##constants - look up how to put just the constants to configure in a different file and use it here

#logging.info('Configuring parameters')
years = range(2018,2020)
document= '10-K'
col_specification = [(0, 61), (62, 73), (74, 85), (86, 97), (98, 159)]
columnHeaders = ['company_name','form_type','cik','date','file_name']

##dataframe_10k_apple = pd.DataFrame(columns = columnHeaders)
dataframe_10k_q = pd.DataFrame(columns = columnHeaders)
dataframe_10k = pd.DataFrame(columns = columnHeaders)
##details_10k = open('details_10k.txt', 'a')

cik_list = []

for year in years: 
    #logging.debug('for each year..')
    for quarter in ['QTR1', 'QTR2', 'QTR3', 'QTR4']:
        #logging.debug('for each quarter')
        indexfile = r'https://www.sec.gov/Archives/edgar/full-index/' + str(year) + '/' + quarter + '/company.idx'

        realindexfile = requests.get(indexfile, allow_redirects=True)
        
        dataframe = pd.read_fwf(StringIO(realindexfile.text), colspecs=col_specification, skiprows=9)
        #dataframe.to_csv('C:\\Users\\Shreya Sainathan\\Downloads\\file_name.csv')
        #name the columns
        dataframe.columns = columnHeaders
        
        if(dataframe_10k.empty == True):            
            dataframe_10k = dataframe[(dataframe['form_type'].str.contains(document))]
        else:       
            dataframe_10k = dataframe_10k.append(dataframe[(dataframe['form_type'].str.contains('10-K'))])
        
    dataframe_10k.to_csv('C:\\Users\\simondong\\Desktop\\99520\\details_10k.csv')
        
print(dataframe_10k.head())

#logging.debug('getting the 10-k data for each company')

cik_list = get_cik_list(dataframe_10k)

for i in range(len(dataframe_10k)) : 
    url = 'https://www.sec.gov/Archives/' + dataframe_10k.iloc[i]['file_name']
    print(url)
    response = requests.get(url)
    response.encoding = 'utf-8'

    clean_txt = remove_html_tags(response.text)
    ##item_1 = r"(Item[\s;]*?1A[.]{0,1}).*?(Risk[\s]+?Factors)"
    ##item_1b = r"Item[\s;]*?1B[.]{0,1}.*?Unresolved[\s]+staff[\s]+comments"
    #item_1b = r"Item.*?1B[.]{0,1}.*?Unresolved[\s]+staff[\s]+comments"
    item_all = "Item[\s;]*?1A[.]{0,1}.{0,10}Risk[\s]+?Factors.*?Item[\s;]*?1B[.]{0,1}.{0,10}Unresolved[\s]+staff[\s]+comments"
    x = re.findall(item_all, clean_txt,flags=re.IGNORECASE|re.DOTALL|re.M)#risk.*factors .*item.*1B.*unresolved.*staff.*comments
    
    
    counts_dictionary = count_words(max_length(x))
    counts_dataframe = pd.DataFrame(counts_dictionary, index=[0])
    to_write = dataframe_10k.iloc[i][['cik', 'company_name', 'date']]
    result = pd.concat([to_write, counts_dataframe], axis=1, sort=False)
    result.to_csv('final_data.csv', mode = 'a')
    

    


