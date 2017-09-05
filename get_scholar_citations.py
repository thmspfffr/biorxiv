
from bs4 import BeautifulSoup
import requests
#from time import sleep

def make_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def get_scholar_link(title):
    """
    transforms paper title to scholar link
    """
    title_split = title.split(" ")
    url = 'https://scholar.google.com/scholar?q="'

    for ititle in range(0,len(title_split)):
        if ititle == 0:
            url = url + "%s" % title_split[ititle]
        else:
            url = url + "+%s" % title_split[ititle]

    return url + '"'

def get_citations(url):
    """
    get number of citations
    """
    text = make_soup(url)
    #info = make_soup(url + ".article-info")
    text = text.find_all("a")

    for itext in range(0,len(text)):

        tmp_text = str(text[itext])

        if tmp_text.find('Cited by ') >= 0:

            tmp_text = tmp_text.split('Cited by ')[1]

            citations = int(tmp_text.split('<')[0])

            break

        else:

            citations = 0
   
    return citations
