# -*- coding: utf-8 -*-

#How to get the HTML
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# main page URL
url = 'https://www.carpages.ca/used-cars/search/?fueltype_id%5B0%5D=3&fueltype_id%5B1%5D=7'

# page request to get the data
page = requests.get(url)

# page respond 200 ok
page
# prepare the soup
soup = BeautifulSoup(page.text, 'lxml')
#soup
soup.prettify()



# prepare 4 lists to fill therequired data
car_description=[]
car_price=[]
car_links=[]
car_colours=[]

# prepare Data frame to contain the data
df=pd.DataFrame({'car_description':[''], 'car_price':[''], 'car_links':[''],\
                'car_colours':['']})
    
# counter for number of pages to be scraped    
counter = 0

#This loop goes through the first 10 pages and grabs all the details of each posting
while counter < 10:
    Adverts=soup.find_all('div',class_='media soft push-none rule')

# loop each advert item to scrap the data (description, link, colour, price)    
    for item in Adverts:
        description=item.find('h4',class_=re.compile('hN')).text.strip()
        price=item.find('strong', class_= 'delta').text.strip()
        link=item.find('a',class_='media__img media__img--thumb').get('href')
        link='https://www.carpages.ca'+link
        colour=item.find_all('span')
        colour1=[i.text.strip() for i in colour if len(i) > 1]

# append the data frame
        df = df.append({'car_description':description, \
                        'car_price':price, \
                        'car_links':link,\
                        'car_colours':colour1}, ignore_index = True)
        
    #grabs the url of the next page
    next_page = soup.find('a', class_ = 'nextprev').get('href')
    
    #Imports the next pages HTML into python
    page = requests.get(next_page)
    soup = BeautifulSoup(page.text, 'lxml')
    counter += 1

#Save data Frame into excell file
df.to_excel("webscraping.xlsx", sheet_name='car_page')
 
            
        

    
    
