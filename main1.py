import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
url="https://en.wikipedia.org/wiki/2022_Uttar_Pradesh_Legislative_Assembly_election"
page=requests.get(url)
htmlContent= page.content

soup =BeautifulSoup(page.text, 'html.parser')

pp= soup.find_all("table", attrs={"class": "wikitable"})
print("Number of tables on site: ",len(pp))

table1 = pp[17]
# the head will form our column names
body = table1.find_all("tr")
# Head values (Column names) are the first items of the body list
head = body[1] # 0th item is the header row
body_rows = body[2:] # All other items becomes the rest of the rows

headings = []
for item in head.find_all("th"): # loop through all th elements
    # convert the th elements to text and strip "\n"
    item = (item.text).rstrip("\n")
    # append the clean column name to headings
    headings.append(item)
print(headings)
# Next is now to loop though the rest of the rows

#print(body_rows[0])
all_rows = [] # will be a list for list for all rows
for row_num in range(len(body_rows)): # A row at a time
    row = [] # this will old entries for one row
    for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
        aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
        #append aa to row - note one row entry is being appended
        row.append(aa)
    # append one row to all_rows
    all_rows.append(row)
print(all_rows) 
sl=[]
name=[]
candidate=[]
party=[]
votes=[]
Per=[]
candidateru=[]
party_ru=[]
votes_ru=[]
per_ru=[]
margin=[]
polling_on=[]

