from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
baris = table.find_all('tr')

row_length = len(baris)

temp = [] #initiating a list 

for i in range(0, row_length):

    #scrapping process
    #get tanggal 
    Tanggal = table.find_all('td')[(i*4)+0].text

    #get nilai kurs
    Kurs = table.find_all('td')[(i*4)+2].text
    Kurs = Kurs.strip() #to remove excess white space
    
    temp.append((Tanggal,Kurs)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('Tanggal','Kurs'))
df['Kurs'] = df['Kurs'].str.replace(" IDR","")
df['Kurs'] = df['Kurs'].str.replace(",","")
df['Kurs'] = df['Kurs'].astype('float64')
df['Tanggal'] = df['Tanggal'].astype('datetime64')
#insert data wrangling here
#set tanggal menjadi index
df = df.set_index('Tanggal')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Kurs"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (15,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)