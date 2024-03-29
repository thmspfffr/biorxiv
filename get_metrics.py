
from bs4 import BeautifulSoup
import requests
#from time import sleep
import datetime
import time

def make_soup(url):
    r = requests.get(url)
    #soup = BeautifulSoup(r.text, 'lxml')
    soup = BeautifulSoup(r.text,'html.parser')
    return soup

def get_num_pages():
    """
    Gets the total number of pages
    """
    # Estimate total duration
    url = "http://www.biorxiv.org/content/early/recent?page=1"
    text = make_soup(url)
    text = text.find_all('a')

    for itext in range(0,len(text)):
        txt = str(text[itext])
        
        if txt.find('Go to page') > 0:
            tmp = txt.split()[5]
            page_no = int(tmp.split('"')[0])
            
    return page_no

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

def is_published(url,driver):
    """
    returns 1 if published
    """
    driver.get(url)
    p = driver.find_element_by_class_name('pub_jnl')

    if 'not been peer-reviewed' in p.text:
        published = 0
    elif 'Now published in':
        published = 1
    else:
        published = 0

    return published

def get_citations(url,driver):
    """
    gets paper citations and doi 
    """
    driver.get(url)
    p = driver.find_element_by_class_name('pub_jnl')

    if 'not been peer-reviewed' in p.text:
        doi = "NA"
    elif 'Now published in':
        doi = p.text[p.text.find('doi')+5:]
        url_dimensions = "https://metrics-api.dimensions.ai/doi/" + doi
        metrics_dimensions = requests.get(url_dimensions).json()
        citations = metrics_dimensions['times_cited']
    else:
        doi = "NA"

    return citations

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
        
        abstract = 0; pdf = 0; abstract_first = 0; pdf_first = 0

        for iview in range(0,len(views)):

            if iview % 3 == 0 and iview != 9:
                continue
            elif iview == 9:
                abstract_first = abstract
                pdf_first = pdf
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
        abstract_first = abstract
        pdf_first = pdf
    else:

        abstract = "NA"
        pdf = "NA" 
        abstract_first = "NA"
        pdf_first = "NA"

    #versions = info.findAll("ul", "issue-toc-list")
    publication_date = (url.split("/")[5:8])
    current_date = datetime.date(int(publication_date[0]), int(publication_date[1]), int(publication_date[2]))
    # compute age of article in days
    age = int((time.time()-time.mktime(current_date.timetuple()))/(3600*24))

    return [abstract, pdf, age, abstract_first, pdf_first]