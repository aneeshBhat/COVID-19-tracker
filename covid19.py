#python data analysis
import numpy as np
import pandas as pd 

#python charts 
import matplotlib.pyplot as plt
import seaborn as sns
 
#python web frame wrok - flask
from flask_restful import Resource, Api
from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
from requests import Session

#Used for Webscraping -- beatifulSoup
from bs4 import BeautifulSoup
import requests

#url for extracting data from website
url_gov = "https://www.mohfw.gov.in/"
web_content = requests.get(url_gov).content

#webscarping
scrap = BeautifulSoup(web_content,"html.parser")
extract_contents = lambda row:[x.text.replace('\n','') for x in row]
stats =[]

#finding all rows in table
all_rows = scrap.findAll('tr')
for row in all_rows:
    stat =   extract_contents(row.findAll('td'))
    if len(stat) == 5:
        #appending data to array
        stats.append(stat)
    
#definig coloumn header
new_cols = ["Sr.No","states/UT","Confirmed","Recoverd","Deceased"]

#Data analysis using pandas 
state_data = pd.DataFrame(data = stats,columns=new_cols)
print(state_data.head(),'webcontent')
state_data['Confirmed'] = state_data['Confirmed'].map(int)

#setting charts style & displaying charts.
sns.set_style("ticks")
plt.figure(figsize=(15,10))
plt.barh(state_data["states/UT"],state_data["Confirmed"].map(int),align='center',color = 'lightblue',edgecolor = 'blue')

#labeling the chart
plt.xlabel('No of Confirmed cases', fontsize = 18)
plt.ylabel('States/UT',fontsize=18) 

plt.gca().invert_yaxis()
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.title("Total Confirmed Cases Statewise",fontsize = 18)

#displaying no of cases of each state  in charts
for index,value in enumerate(state_data["Confirmed"]):
    plt.text(value,index,str(value),fontsize=10)

 
#run the chart
plt.show()



# --------------------------- PART 2 / Rest api for Angular -------------------------------

url = "https://www.worldometers.info/coronavirus/"

req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
table = soup.find('table')
rows= table.findAll('tr')
th=table.findAll('th')
# th.findChildren(text=True)
header = [[u"".join(td) for td in t] for t in th]
header=[" ".join(d) for d in header]
print(header,'data')
data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
print(len(data))
data = [[u"".join(d) for d in l] for l in data]
s=pd.DataFrame(data,columns=header)
fig = plt.figure(figsize=(15, 10)) 

#setup for flask frame Work

app = Flask(__name__)
api = Api(app)
CORS(app)
@app.route("/")
def getData():
    return  {'employess':data}
    # jsonify({'text':'Stay Home!'})


if __name__ == '__main__':
     app.run(port=5002)