import requests, re
from bs4 import BeautifulSoup


def getURL(url):
    response = requests.get(url)
    return response

def scrapeWikiTableFromHTML(html_page):
    soup = BeautifulSoup(html_page.content, "html.parser")
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    sub_data=[]
    index = 0
    for row in rows:
        cols = row.find_all('td')
        for col in cols:
            if (index==0):
                sub_data=[]
                element = col.text.strip()
                element_clean = re.sub('((\[|\()[a-zA-Z0-9\s]*(\]|\)))', '', element)
                sub_data.append(element_clean)

            if (index==4):
                element = col.text.strip()
                element_clean = element.replace(",", "")
                if (element_clean.isnumeric()):
                    element_clean = int(element_clean)
                sub_data.append(element_clean)
                data.append(sub_data)
            index=(index+1)%6
    return data
wiki_url = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"

page = getURL(wiki_url)
table = scrapeWikiTableFromHTML(page)


