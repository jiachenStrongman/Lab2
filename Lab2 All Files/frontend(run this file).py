#front end file for lab2

import Backend as be
import tkinter as tk
import tkinter.font as font
import matplotlib.pyplot as plt
import numpy as np

menu = tk.Tk()
menu.title("TOP 10 COUNTRIES FOSSIL CO2 EMISSIONS IN 2017 (% OF WORLD)")
menu.geometry("550x400")

prompt = tk.Label(menu, text = "CLICK TO SEE A COOL PIE CHART", font = ("helvetica, 25"))
prompt.grid()

topTen = []
topPerc = []
for i in range(10):
#populates the two lists with percentages and countries
    topTen.append(be.countryDB.sort()[i][0])
    topPerc.append(be.countryDB.sort()[i][1])


#function for the button to show the graph
def gogo():
    fig = plt.figure(figsize = (10, 5))
    plt.pie(topPerc, labels = topTen, autopct = '%1.2f%%')
    plt.title("Top 10 countries by fossil CO2 emissions (% of world)")
    plt.show()

#button for the user interface
butFont = font.Font(family = 'Helvetica', size = 50)
chartButt = tk.Button(menu, text = "CLICK HERE", padx = 25, pady = 75, bg = '#f65909', fg = '#0cc8f3', command = gogo)
chartButt['font'] = butFont
chartButt.grid()
