#Backend File for Lab2 Web Scraping

from bs4 import BeautifulSoup
import requests
import pandas as pd
import webbrowser
import sqlite3

#webbrowser.open('https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions')

site = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions').text
soup = BeautifulSoup(site, 'html.parser')

table = soup.find('table', class_='wikitable sortable') #gets the correct table from wikipedia page

#database class and it's functions from lab 1
class database:
    def __init__(self, carbDB): #connect and initialize class function
        self.carbDB = sqlite3.connect('carbon.db')
        cursor = self.carbDB.cursor()
        print("Database connected")
        cursor.close()
        if(self.carbDB):
            self.carbDB.close()

    def table(self):
        self.carbDB = sqlite3.connect('carbon.db')
        carbTable = '''CREATE TABLE carbTable(
                    COUNTRY TEXT PRIMARY KEY,
                    EMISSIONS TEXT,
                    DECIMAL REAL);''' #adding a decimal value that is the emissions percentage without the %
        cursor = self.carbDB.cursor()
        print("table created")
        cursor.execute(carbTable)
        self.carbDB.commit()
        if(self.carbDB):
            self.carbDB.close()

    def insert(self, country, fossil, dec):
        self.carbDB = sqlite3.connect('carbon.db')
        cursor = self.carbDB.cursor()
        insertTab = '''INSERT INTO carbTable
                    (COUNTRY, EMISSIONS, DECIMAL) VALUES (?, ?, ?)'''
        data_tuple = (country, fossil, dec)
        cursor.execute(insertTab, data_tuple)
        self.carbDB.commit()
        cursor.close()
        if(self.carbDB):
            self.carbDB.close()

    def search(self):
        self.carbDB = sqlite3.connect('carbon.db')
        cursor = self.carbDB.cursor()
        cursor.execute('''SELECT COUNTRY, DECIMAL FROM carbTable''')
        result = cursor.fetchall()
        return result

    def sort(self): #will return a sorted version of the database
        self.carbDB = sqlite3.connect('carbon.db')
        cursor = self.carbDB.cursor()
        sortTable = '''SELECT COUNTRY, EMISSIONS, DECIMAL
                    FROM carbTable
                    ORDER BY DECIMAL DESC; '''
        cursor.execute(sortTable)
        print("Database sorted")
        sortDB = cursor.fetchall()
        self.carbDB.commit()
        cursor.close()
        return sortDB

    def checkTable(self): #checks to see if the table is already there
        self.carbDB = sqlite3.connect('carbon.db')
        cursor = self.carbDB.cursor()
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name = 'carbTable' ''')
        if(cursor.fetchone()[0] == 1):
            return False
        else:
            return True
        cursor.close()
        if(self.carbDB):
            self.carbDB.close()

countryDB = database([]) #initialize the database

if(countryDB.checkTable()):
    countryDB.table() #creates table

    #inserts wikipedia table data
    counter = 0 #this is a counter to skip the first 3 rows 
    for row in table.tbody.find_all('tr'):
        counter += 1
        columns = row.find_all('td')
        if(counter > 5): #starts storing the data starting from the countries and not the world data
            if(columns != []):
                country = columns[0].text.strip()
                percent = columns[4].text.strip()
                decimal = float(percent[:len(percent) - 1]) #i need a decimal value to sort
                countryDB.insert(country, percent, decimal) #takes data from 5th column since thats the only data i need
