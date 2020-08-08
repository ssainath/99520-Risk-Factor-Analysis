from bs4 import BeautifulSoup
import requests
import re 
import pandas as pd
import numpy as np
from io import StringIO
import requests
import re

df = pd.read_csv("2007copy.csv", dtype={"cik": pd.Int64Dtype()}, skiprows=lambda x: (x != 0) and not x % 2)
companydata = pd.read_csv("wrds data.csv", dtype={"fyear": pd.Int64Dtype() ,"cik": pd.Int64Dtype()}, usecols=["conm", "cik","fyear", "at", "ni", "roa"], na_values = ".")

companydata = companydata[['cik', 'conm', 'fyear', "at", "ni", "roa"]]
companydata.to_csv("betterroa.csv", index = False)

final = df.copy()
final.reset_index(drop=True)

final["at"] = ""
final["ni"] = ""
final["roa"] = ""
del final['Unnamed: 0']


linenumber = 0
list_of_lists = []


# def getcsv():
#     from csv import reader
#     with open('2007copy.csv', 'r') as read_obj:
#         csv_reader = reader(read_obj)
#         for row in csv_reader:
#         print(row[0])
#         if row[0] == "0":
#             cik1= row[1]
#             print("cik1 is")
#             print(cik1)
#             date = row[3]
#             year1 = date[:4]
#             return (cik1, year1)

# def getroa():
#     while (line != ""):
#         line = company.readline()
#         column = re.split(r'\s{2,}', line)
#         if (len(column)>7):
#             if linenumber != 0:
#                 cikunstripped = column[4]
#                 cik2 = cikunstripped.strip("0")
#                 year2 = column[2]
#                 if (column[6] != ".") and (column[5] != ".") and (column[6] != "C") and (column[5] != "C") and (column[6] != "0.0000") and (column[5] != "0.0000"):
#                     roa = float(column[6])/(float(column[5]))
#                 else:
#                     roa = "."
#     return (cik2, year2, roa)

# def match():



for index, row in final.iterrows():
    cik = row.loc['cik']
    date = row.loc['date']
    year = int(date[:4])
    wordnumber = row.loc['total words']
    if (wordnumber<100):
        final.drop([index], axis=0, inplace=True)
        continue

    found = companydata.loc[companydata['cik'] == cik]
    if not (found.empty):
        #now match year
        foundyear = found.loc[found['fyear'] == year]
        if not (foundyear.empty):
            '''
            if (foundyear.iloc[0]['at'] == ""):
                final.drop([index], axis=0, inplace=True)
                continue
            '''
            final.loc[index, 'at'] = foundyear.iloc[0]['at']
            final.loc[index, 'ni'] = foundyear.iloc[0]['ni']
            final.loc[index, 'roa'] = foundyear.iloc[0]['roa']
        else:
            final.drop([index], axis=0, inplace=True)
    else:
        final.drop([index], axis=0, inplace=True)
        
            
final.to_csv("merged data.csv")

# newfile.close()
