import sys
import random

import requests
from fpdf import FPDF

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from requests import HTTPError
from html.parser import HTMLParser

colours = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120), (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150)]
title = "Athens - report for January 2019"
# create the pdf


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'image':
            for attr in attrs:
                if attr[0] == 'src':
                    addGraph(attr[1])

    def handle_data(self, data):
        data = data.encode('latin-1', 'replace').decode('latin-1')
        addText(data)

class PDF(FPDF):
    def header(self):
        self.set_fill_color(3, 19, 49)
        self.rect(0, 0, self.w, self.h, "F")

pdf = PDF("P", "mm", "A4")

for i in range(len(colours)): # Matplotlib uses 0-1 range instead of 0-255
    r, g, b = colours[i]
    colours[i] = (r / 255., g / 255., b / 255.)

def fetchUSdata():
    y = []
    x = []

    # Make sure that the call was successful
    try:
        response = requests.get("http://api.worldbank.org/v2/country/us/indicator/SP.POP.TOTL?format=json")
        response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        sys.exit()

    except Exception as err:
        print(f'Other error occurred: {err}')
        sys.exit()

    else:  # View the data
        JSONdata = response.json()
        country = JSONdata[1][0]['country']['id']
        for data in JSONdata[1]:
            if data['value'] != None:
                x.append(data['date'])
                y.append(data['value']/1000000)

        return x, y, country


def fetchUKdata():
    y = []
    x = []

    # Make sure that the call was successful
    try:
        response = requests.get("http://api.worldbank.org/v2/country/gb/indicator/SP.POP.TOTL?format=json")
        response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        sys.exit()

    except Exception as err:
        print(f'Other error occurred: {err}')
        sys.exit()

    else:  # View the data
        JSONdata = response.json()
        country = JSONdata[1][0]['country']['id']
        for data in JSONdata[1]:
            if data['value'] != None:
                x.append(data['date'])
                y.append(data['value']/1000000)

        return x, y, country


def fetchESdata():
    y = []
    x = []

    # Make sure that the call was successful
    try:
        response = requests.get("http://api.worldbank.org/v2/country/es/indicator/SP.POP.TOTL?format=json")
        response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        sys.exit()

    except Exception as err:
        print(f'Other error occurred: {err}')
        sys.exit()

    else:  # View the data
        JSONdata = response.json()
        country = JSONdata[1][0]['country']['id']
        for data in JSONdata[1]:
            if data['value'] != None:
                x.append(data['date'])
                y.append(data['value']/1000000)

        return x, y, country


def createGraph(x,y, country):
    # Make the graph pretty
    plt.figure(figsize=(20, 7.5))
    plt.gcf().subplots_adjust(bottom=0.15)# make room for x lable

    # Get rid of top and right border
    ax = plt.subplot(111)
    ax.set_title(country, fontsize=40, color='w')
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%1dM'))
    ax.tick_params(colors=(82/255,159/255,184/255))
    ax.set_ylabel('Population', color="w", fontsize=30,labelpad=20)
    ax.set_xlabel('Years', color="w", fontsize=30,labelpad=20)
    yx = 0
    for i in range(0, int(max(y)), 10):
        ax.axhline(y=i, color=(51/255,65/255,90/255))
        yx = i
    yx+= 10
    ax.axhline(y=yx,color=(51/255,65/255,90/255))

    plt.yticks(fontsize=20)
    plt.xticks(range(0, 70, 8), fontsize=26)
    plt.gca().invert_xaxis()

    # Plot/Save the graph
    # Set a "random" colour for each line (in a real report the colours will have to be
    # pre determined to keep them consistent over all downloaded reports)
    #with plt.rc_context({'xtick.color': 'red', 'ytick.color': 'green'}):
    plt.plot(x, y, color = (237/255,121/255,51/255), linewidth=7)
    #plt.show()
    plt.savefig('graphs/'+country + '.png', transparent = True)

    return country + '.png'

def addText(text):

    pdf.multi_cell(0,6,text)
    h = pdf.get_y()
    pdf.set_y(h)

def addGraph(graph):

    h = pdf.get_y()
    if h+75 > pdf.h:
        pdf.add_page()
        h = pdf.get_y()
    pdf.image(graph, 5, h, 200, 75)
    pdf.set_y(h+75)

def createTitlePage(pdf, title):
    pdf.add_page()

    pdf.image('images/logo.jpg', 30,25,150)
    pdf.image('images/title_image.jpg', 0, 75, pdf.w)

    pdf.set_font('Arial', '', 15)
    pdf.set_xy(0,255)
    pdf.cell(pdf.w,0, title, align="C")

    return pdf

if __name__== "__main__":
    graphs = []
    parser = MyHTMLParser()

    pdf.set_text_color(255, 255, 255)
    pdf = createTitlePage(pdf, title)
    pdf.add_page()
    pdf.set_font('Arial', '', 11)
    file = open('text.html', 'r')
    parser.feed(file.read())
    file.close()
    #Fetch all the data
    x,y, id = fetchUSdata()
    img = createGraph(x,y, id)

    x, y, id = fetchUKdata()
    img = createGraph(x, y, id)

    x, y, id = fetchESdata()
    img = createGraph(x, y, id)

    pdf.output('Report.pdf', 'F')