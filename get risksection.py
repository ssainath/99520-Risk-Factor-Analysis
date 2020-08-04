from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import requests
import re

'''

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
        "pandemic" : 0,
        "total words" : 0}
    return dict

def count_words(item_1a_section):
    counts= fill_dictionary()
    words = item_1a_section.split()
    for word in words:
        counts['total words'] +=1
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

'''


years = range(2018,2020)
document= '10-K'
col_specification = [(0, 61), (62, 73), (74, 85), (86, 97), (98, 159)]
columnHeaders = ['company_name','form_type','cik','date','file_name']

#txt file to store all the risk sections
risksection = open(r"2019risksections.txt", mode = "a+")


dataframe_10k_q = pd.DataFrame(columns = columnHeaders)
dataframe_10k = pd.DataFrame(columns = columnHeaders)
# store all the 10ks that the code didnt work for
problem_10k = pd.DataFrame(columns = columnHeaders)



for year in years: 

    for quarter in ['QTR1', 'QTR2', 'QTR3', 'QTR4']:

        indexfile = r'https://www.sec.gov/Archives/edgar/full-index/' + str(year) + '/' + quarter + '/company.idx'

        realindexfile = requests.get(indexfile, allow_redirects=True)
        realindexfile.encoding = 'utf-8'
        
        dataframe = pd.read_fwf(StringIO(realindexfile.text), colspecs=col_specification, skiprows=9)

        #name the columns
        dataframe.columns = columnHeaders

        if(dataframe_10k.empty == True):            
            dataframe_10k = dataframe[(dataframe['form_type']==(document))]
        else:       
            dataframe_10k = dataframe_10k.append(dataframe[(dataframe['form_type']==(document))])
        
    dataframe_10k.to_csv('10-Ks.csv')

print(dataframe_10k.head())

#iterate all 10ks in dataframe
for i in range(len(dataframe_10k)) : 
    url = 'https://www.sec.gov/Archives/' + dataframe_10k.iloc[i]['file_name']

    response = requests.get(url)
    response.encoding = 'utf-8'

    goodsoup = False
    #error handle parser failure
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        problem_10k = pd.concat([problem_10k, dataframe_10k.iloc[[i]]], axis=1, ignore_index=True)
        goodsoup = True

    if goodsoup:
        continue

    #this finds all the unresolved staff comments, ideally this only returns two objects, one in catalog and the actual section
    divlist = soup.find_all("div", string = re.compile("Unresolved Staff Comments", flags=re.IGNORECASE))
    if (len(divlist)<2):
        problem_10k = pd.concat([problem_10k, dataframe_10k.iloc[[i]]], axis=1, ignore_index=True)
        continue
        
    theone = divlist[1]

    found = True
    goodsection = True
    clean = re.compile('<.*?>')

    thisrisksection = ""

    #this will write the risk section but backwards...
    while found:
        prevdiv = theone.previous_sibling
        if (prevdiv==None):
            problem_10k = pd.concat([problem_10k, dataframe_10k.iloc[[i]]], axis=1, ignore_index=True)
            goodsection = False
            break
            
        prevdivtext = str(prevdiv)

        thisrisksection = thisrisksection + prevdivtext + "\n"

        #check if we reached risk factors header
        if (re.search(re.compile("risk factors", flags=re.IGNORECASE), prevdivtext) != None):
            prevdivtext = re.sub(clean, '', prevdivtext)
            #print(prevdivtext)
            if (len(prevdivtext)<35):
                found = False
        #iterate
        theone = prevdiv

    #no problem with risk section
    if goodsection:
        # two line seperation bewtwen companies
        risksection.write(thisrisksection + dataframe_10k.iloc[[i]].to_string() + "\n\n")
        #update the file
        risksection.flush()


problem_10k.to_csv('problem10ks.csv', index=True)
risksection.close()

    
    #item_all = "Item[\s;]*?1A[.]{0,1}.{0,10}Risk[\s]+?Factors.*?Item[\s;]*?1B[.]{0,1}.{0,10}Unresolved[\s]+staff[\s]+comments"
    #x = re.findall(item_all, clean_txt,flags=re.IGNORECASE|re.DOTALL|re.M)#risk.*factors .*item.*1B.*unresolved.*staff.*comments

    #counts_dictionary = count_words(max_length(x))
    #counts_dataframe = pd.DataFrame(counts_dictionary, index=[0])
'''
    to_write = dataframe_10k.iloc[[i]][['cik', 'company_name', 'date']]
    to_write.index = [0]
    result = pd.concat([to_write, counts_dataframe], axis=1, sort=False)
    result.to_csv('final_data.csv', mode = 'a')
'''


