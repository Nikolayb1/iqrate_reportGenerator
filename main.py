import sys
import random

import requests
from fpdf import FPDF

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from requests import HTTPError

colours = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120), (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150)]

for i in range(len(colours)): # Matplotlib uses 0-1 range instead of 0-255
    r, g, b = colours[i]
    colours[i] = (r / 255., g / 255., b / 255.)

# Set the Title in the Header and page number in the footer
class PDF(FPDF):
    def header(self):

        self.set_font('Arial', 'B', 15)
        self.cell(80)

        self.cell(30, 10, 'Report With Grpahs', 0, 0, 'C')
        self.set_font('Arial', '', 7)
        self.cell(-30, 25, '06/02/2020', 0, 0, 'C')

        self.ln(20)


    def footer(self):

        self.set_y(-15)

        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, str(self.page_no()), 0, 0, 'C')

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

    else:# View the data
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

    else:# View the data
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

    else:# View the data
        JSONdata = response.json()
        country = JSONdata[1][0]['country']['id']
        for data in JSONdata[1]:
            if data['value'] != None:
                x.append(data['date'])
                y.append(data['value']/1000000)

        return x, y, country


def createGraph(x,y, country):
    # Make the graph pretty
    plt.figure(figsize=(12, 9))

    # Get rid of top and right border
    ax = plt.subplot(111)
    ax.set_title(country, fontsize=30)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%1dM'))

    plt.yticks(fontsize=16)
    plt.xticks(range(0, 70, 8), fontsize=16)
    plt.gca().invert_xaxis()

    # Plot/Save the graph
    # Set a "random" colour for each line (in a real report the colours will have to be
    # pre determined to keep them consistent over all downloaded reports)
    plt.plot(x, y, color = colours[random.randint(0, len(colours)-1)])
    plt.savefig(country + '.png')

    return country + '.png'

def addSection(pdf, img, textPos, imgPos):
    pdf.image(img, 5, imgPos, 100, 75)
    pdf.set_xy(100, textPos)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 4,'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut '
                        'labore et dolore magna aliqua. Pellentesque pulvinar pellentesque habitant morbi tristique. Et '
                        'tortor consequat id porta. Vitae aliquet nec ullamcorper sit amet risus nullam. Magna fermentum'
                        ' iaculis eu non diam phasellus. Pellentesque sit amet porttitor eget dolor morbi non. Mattis '
                        'aliquam faucibus purus in. Velit laoreet id donec ultrices tincidunt arcu non. In nulla posuere'
                        ' sollicitudin aliquam ultrices. Feugiat nisl pretium fusce id. In hac habitasse platea dictumst '
                        'quisque.')
    return pdf

if __name__== "__main__":
    graphs = []


    x,y, id = fetchUSdata()
    img = createGraph(x,y, id)
    graphs.append(img)

    x, y, id = fetchUKdata()
    img = createGraph(x, y, id)
    graphs.append(img)

    x, y, id = fetchESdata()
    img = createGraph(x, y, id)
    graphs.append(img)

    # create the pdf
    pdf = PDF()
    pdf.add_page()

    textPos = 40
    imgPos = 30

    for im in graphs:
        pdf = addSection(pdf, im, textPos, imgPos)
        textPos += 80
        imgPos += 80

    pdf.output('Report.pdf', 'F')


