
from bs4 import BeautifulSoup
import requests
#from time import sleep
import datetime
import time

def make_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def get_paper_links(url):
    """
    gets paper title and link for each paper on page
    apply to each page in archive
    """
    soup = make_soup(url)
    div = soup.findAll("div", "highwire-list")
    links = []
    for date in div:
        for i in date.findAll("li"):
            try:
                i.a.string
            except:
                pass
            else:  # hack
                if i.a.string == None:
                    pass
                elif len(i.a.string) < 5:
                    pass
                else:
                    links.append({"title": i.a.string, 
                                  "link": i.a["href"]})
    return links

def get_title(url):
    """
    gets paper title and link for each paper on page
    apply to each page in archive
    """
    soup = make_soup(url)
    div = str(soup.findAll("div", "highwire-cite-title")[0])
    text = div.split('>')
    text = text[2]
    title = text.split('<')[0]
    
    return title

def get_metrics(url):
    """
    get number of abstract view and PDF downloads
    Not all papers have this, only after a certain length of time
    Also get when it was first posted and the date most recent version was posted
    """
    
    metrics = make_soup(url)
    #info = make_soup(url + ".article-info")
    views = metrics.findAll("td")

    if len(views) > 5:
        abstract = 0
        pdf = 0
        for iview in range(0,len(views)):

            if iview % 3 == 0:
                continue
            elif iview % 3 == 1:
                s = str(views[iview])
                s = s.split('>')[1]
                num = int(s.split('<')[0])
                abstract = abstract + num
            elif iview % 3 == 2:
                s = str(views[iview])
                s = s.split('>')[1]
                num = int(s.split('<')[0])
                pdf = pdf + num

    elif (len(views) < 5) and (len(views) >= 3):
        abstract = int(views[1].text)
        pdf = int(views[2].text)

    else:

        abstract = "NA"
        pdf = "NA" 

    #versions = info.findAll("ul", "issue-toc-list")
    publication_date = (url.split("/")[5:8])
    current_date = datetime.date(int(publication_date[0]), int(publication_date[1]), int(publication_date[2]))
    # compute age of article in days
    age = int((time.time()-time.mktime(current_date.timetuple()))/(3600*24))

    return [abstract, pdf, age]