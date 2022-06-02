from tkinter.tix import InputOnly
from xml.sax.xmlreader import InputSource
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import mysql.connector
import mysql.connector as msql
from mysql.connector import Error
url="https://en.wikipedia.org/wiki/2022_Uttar_Pradesh_Legislative_Assembly_election"
page=requests.get(url)
htmlContent= page.content

soup =BeautifulSoup(page.text, 'html.parser')
pp= soup.find_all("table", attrs={"class": "wikitable"})
table1 = pp[17]

#The head will form our Column Names

body = table1.find_all("tr")

#Head values (Column names) are the first items of the body list
head = body[1] #0th item is the header row
body_rows = body[2:] #All other items becomes the rest of the rows

headings = []
for item in head.find_all("th"): #Loop through all th elements
    # Convert the th elements to text and strip "\n"
    item = (item.text).rstrip("\n")
    # Append the clean column name to headings
    headings.append(item)
# Next is now to loop though the rest of the rows

all_rows = [] # Will be the list for list for all rows
for row_num in range(len(body_rows)): # One row at a time
    row = [] # This will old out the entries for one row
    for row_item in body_rows[row_num].find_all("td"): #Loop through all row entries
        aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
        #Append aa to row - note one row entry is being appended
        row.append(aa)
    # Append one row to all_rows
    all_rows.append(row) 
sl=[]
district=[]
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
for i in all_rows:
    if(len(i)==13 or len(i)==12):
        candidate.append(str(i[1]))
        name.append(str(i[0]))
        party.append(str(i[3]))
        votes.append(str(i[4]))
        Per.append(str(i[5]))
        candidateru.append(str(i[6]))
        party_ru.append(str(i[8]))
        votes_ru.append(str(i[9]))
        per_ru.append(str(i[10]))
        margin.append(str(i[11]))      
l=0
for i in all_rows:
    if(len(i)==13 or len(i)==12):
        l=l+1
        sl.append(str(l))
for i in all_rows:
        if (len(i)==1):
            s=i[0]
        if (len(i)==13):
            v=i[12]
        if (len(i)==12 or len(i)==13):
                district.append(str(s))
                polling_on.append(str(v))
percentage_margin=[]
temp=0
for i in range (0, len(name)):
        temp=float (Per[i]) - float (per_ru[i])
        percentage_margin.append(str(f'{temp:.2f}'))
#District decided for
miin=0
maax=0
val=input("Enter Your District: ")
for i in range (len(district)):
        if district[i]==val:
            miin=i 
            break
for i in range (len(district)):
        if district[i]==val:
            maax=i
fortnite=0
pMargin=int(fortnite)
for i in range(miin,maax):
    temp=percentage_margin[i]
    if pMargin < float(temp):
        pMargin = float(temp)
print("Maximum margin for "+ val +" is "+str(pMargin))

#Election Prediction
val2=input("Enter Your Party Name?  ")
print()
print ("Constituency----Party----Margin")
max_margin=0
max_m=int(0)
min_m=int(0)
min_margin=0 
constituency=[] 
Party=[] 
Margin=[]
for i in range(len(party_ru)):
    if val2==party_ru[i]:
        constituency.append(name[i])
        Party.append(party[i]) 
        Margin.append(margin[i])
        print (name[i]+"----"+party[i]+ "----"+ margin[i])
        if int(max_margin) < int(margin[i]):
            max_m=i
            max_margin=margin[i]
min_margin=max_margin
for i in range(len(party_ru)):
    if val2==party_ru[i]:
        if int(min_margin) > int(margin[i]):
            min_m=i
            min_margin=margin[i]
dictionary={'Constituency': constituency, 'Party': Party, 'Margin': Margin}
df=pd.DataFrame(dictionary)
to_csv=df.to_csv('C:/Users/ahmad/Desktop/runnerup.csv')
print ("There is a high possibility of " + val2 + " winning in "+ name[min_m] + " in next Election")
print ("There is a low possibility of " + val2 + " winning in " + name[max_m] + " in next Election")
print ("These Are The Places Where " +val2+ "  Can Win in the Next Election "  )
val3=input("Enter Your Party Name?  ")
print()
print ("Constituency----Party----Margin")
max_margin=0
max_m=int(0)
min_m=int(0)
min_margin=0
constituency_winner=[] 
Party_winner=[] 
Margin_winner=[]
for i in range(len(party)):
    if val3==party[i]:
        constituency_winner.append(name[i])
        Party_winner.append(party[i]) 
        Margin_winner.append(margin[i])
        print (name[i]+"----"+party_ru[i]+ "----"+ margin[i])
        if int(max_margin) < int(margin[i]):
            max_m=i
            max_margin=margin[i]
min_margin=max_margin
for i in range(len(party)):
    if val3==party[i]:
        if int(min_margin) > int(margin[i]):
            min_m=i
            min_margin=margin[i]
dictionary={'Constituency': constituency_winner, 'Party': Party_winner, 'Margin': Margin_winner}
df=pd.DataFrame(dictionary)
to_csv=df.to_csv('C:/Users/ahmad/Desktop/winner.csv')
print ("There is a high possibility of " + val3 + " winning at "+ name[max_m] + " even in next Election")
print ("There is a low possibility of " + val3 + " winning at " + name[min_m] + " in next Election")
print ("These Are The Places Where " +val3+ "  won in previous Election "  )
#Election Prediction
dictionary={'sno':sl, 'DISTRICT': district, 'NAME':name, 'WINNERCANDIDATE':candidate, 'WINNERPARTY':party, 'WINNERVOTES':votes, 'WINNERPERCENTAGE':Per, 'RUNNERUPVOTES': votes_ru,'RUNNERUPCANDIDATE': candidateru,'RUNNERUPPARTY': party_ru,'RUNNERUPPERCENTAGE': per_ru, 'MARGIN': margin,'percentage_margin': percentage_margin, 'POLLING_ON': polling_on}
df=pd.DataFrame(dictionary)
to_csv=df.to_csv('C:/Users/ahmad/Desktop/db_election.csv')
#Saving data to MySQL database
print("Connecting to Database to save records.......")
#empdata = pd.read_csv('C:\\Users\\ahmad\\Desktop\\db_election.csv', index_col=False, delimiter = ',')
#empdata.head()
#try:
    #conn=mysql.connector.connect(host='127.0.0.1', user= 'root', password ='Ahmad@04', database='election_db', port=3306)
    #if conn.is_connected():
        #cursor = conn.cursor()
        #cursor.execute("select database();")
        #record = cursor.fetchone()
        #print("You're connected to database: ", record)
        #cursor.execute('DROP TABLE IF EXISTS election_table;')
        #print('Creating table....')
        #cursor.execute("CREATE TABLE election_table(no varchar(255), SL_NO varchar(255),DISTRICT varchar(255),NAME varchar(255),CANDIDATE varchar(255),PARTY varchar(255),WINNER_VOTES varchar(255),PERCENTAGE varchar(255),RUNNERUP_CANDIDATE varchar(255),RUNNERUP_PARTY varchar(255),RUNNERUP_VOTES varchar(255),RUNNERUP_PERCENTAGE varchar(255),MARGIN varchar(255), PERCENTAGE_MARGIN varchar(255), POLLING_DATE varchar(255))")
        #print("Table is created....")
        #for i,row in empdata.iterrows():
            #add_votes="INSERT INTO election_db.election_table VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #cursor.execute(add_votes, tuple(row))
        #print("Record inserted")
        #conn.commit()
#except Error as e:
            #print("Error while connecting to MySQL", e)
#Plotting Graphic Representation
import pandas as pd
from matplotlib.pyplot import pie, axis, show
df = pd.read_csv ('db_election.csv')
sums = df.groupby(df["DISTRICT"])["RUNNERUPPERCENTAGE"].sum()
axis('equal');
pie(sums, labels=sums.index);
show()