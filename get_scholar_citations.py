
from bs4 import BeautifulSoup
import requests
#from fake_useragent import UserAgent
import random
#from time import sleep

def make_soup(url):
    #ua = UserAgent()
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def do_nonesense():

    # first request 
    make_soup("http://scholar.google.com")
    word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = requests.get(word_site)
    words = response.content.splitlines()
    word = words[random.randint(1,len(words))]
    url = 'https://scholar.google.com/scholar?q='
    url = url + "%s" % word.decode("utf-8")
    make_soup(url)

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
