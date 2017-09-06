
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
#from time import sleep

def make_soup(url):
    #ua = UserAgent()
    #headers = str(ua.chrome)
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

    if len(text)<4:

        a=str(text[0])

        # indicates google time out due to too many requests
        # find more permanent solution
        
        if a.find('Why did this happen?')>0:

            citations = 9999

            return citations

    else:

        for itext in range(0,len(text)):

            tmp_text = str(text[itext])

            if tmp_text.find('Cited by ') >= 0:

                tmp_text = tmp_text.split('Cited by ')[1]

                citations = int(tmp_text.split('<')[0])

                break

            else:

                citations = 0
   
        return citations
