import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress

#uses any merged csv
df = pd.read_csv("2015-2019 final merged.csv", dtype={"cik": pd.Int64Dtype(), "total words": pd.Int64Dtype(), 'roa': float})

#make columns lists of values (remember to change the column into floats with dtype ^)
roa = df['roa'].tolist()
uncertain = df['uncertain'].tolist()
totalwords = df['total words'].tolist()
'''
#you can do this to any two cols in the data
plt.scatter(uncertain, roa, s=1)
uncertainaxes = plt.gca()
uncertainaxes.set_ylim([-10,10])


plt.ylabel('return on assets')
plt.xlabel('number of mentions of word "uncertain"')
plt.title('return on assets vs metions of "uncertain"')
plt.grid()

plt.show()

'''

#scatter plot, s is size
plt.scatter(totalwords, roa, s=1)

#label axis
plt.ylabel('return on assets')
plt.xlabel('word count of section 1A risk factors')
plt.title('return on assets vs total word count')
#show grid lines
plt.grid()

wordsaxes = plt.gca()
#set x,y axis limits
wordsaxes.set_xlim([0,80000])
wordsaxes.set_ylim([-10,10])

plt.show()
#if you want to save the graph just click the save window shown

