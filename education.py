# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 10:42:58 2015

@author: Administrator
"""

from bs4 import BeautifulSoup

import requests
import pandas as pd
import numpy as np
import sqlite3 as lite

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)

soup = BeautifulSoup(r.content)
soup = soup('table')[6]

# create an empty dataframe
df = pd.DataFrame(columns=['Country','Year','Total','Men','Women'])

# iterate thru the tr records and insert the data in to the dataframe
j = 0
for i in soup.findAll('tr')[8:-11]:
    col = i.findAll('td')
    #print col[0].text
    #print col[1].text
    #print col[4].text
    #print col[7].text
    #print col[10].text
    df.loc[j] = [col[0].text,col[1].text,col[4].text,col[7].text,col[10].text]
    j += 1 
    
# convert the numbers from text to integers
df['Men'] = df['Men'].astype(np.int64)
df['Women'] = df['Women'].astype(np.int64)
df['Total'] = df['Total'].astype(np.int64)

# insert the dataframe data into a SQLite database
con = lite.connect('education.db')
cur = con.cursor()

df.to_sql(con=con, name='school_life', if_exists='replace', flavor='sqlite')