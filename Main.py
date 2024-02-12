import requests, re
from bs4 import BeautifulSoup
import json

def getURL(url):
    response = requests.get(url)
    return response

def scrapeWikiTableFromHTML(html_page):
    soup = BeautifulSoup(html_page.content, "html.parser")
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    index = 0
    for row in rows:
        cols = row.find_all('td')
        for col in cols:
            if (index==0):
                data_dict={}
                element = col.text.strip()
                element_clean = re.sub('((\[|\()[a-zA-Z0-9\s]*(\]|\)))', '', element)
                data_dict["Country"]=element_clean

            if (index==4):
                element = col.text.strip()
                element_clean = element.replace(",", "")
                if (element_clean.isnumeric()):
                    element_clean = int(element_clean)
                data_dict["Population"]=element_clean
                data.append(data_dict)
            index=(index+1)%6
    return data

def runWebScraper(url):
    page = getURL(wiki_url)
    return scrapeWikiTableFromHTML(page)

wiki_url ="https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"

table = runWebScraper(wiki_url)

print(json.dumps(table))


