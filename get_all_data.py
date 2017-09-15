# get data
import get_metrics as gm
import get_scholar_citations as scholar
import numpy as np
import os
from sys import platform
from time import sleep
import random
#
count = 0
inp = []

if platform == "darwin":

    if os.path.isfile('biorxiv_metrics.txt'):
        while True:
            
            #inp = input("Data already exists: (o)verwrite or (c)reate copy? ")
            if inp == 'o' or inp == 'O':
                os.remove('biorxiv_metrics.txt')
                data_to_write = open('biorxiv_metrics.txt','w')
                data_to_write.close()
                break
            elif inp == 'c' or inp == 'C':
                os.rename('biorxiv_metrics.txt','biorxiv_metrics1.txt')
                data_to_write = open('biorxiv_metrics.txt','w')
                data_to_write.close()
                break
            else:
                inp = input("Please indicate your choice. \nData already exists: (o)verwrite or (c)reate copy? ")
    else:
        data_to_write = open('biorxiv_metrics.txt','w')
        data_to_write.close()

else:
    os.remove('biorxiv_metrics.txt')
    data_to_write = open('biorxiv_metrics.txt','w')
    data_to_write.close()

num_of_pages = gm.get_num_pages()

for ipage in range(1000,num_of_pages):

    percent_done = 100*(ipage+1)/(num_of_pages+1)

    print('%0.2f%% done' % percent_done,'\r')

    sleep(random.randint(90,120))

    all_papers = gm.get_paper_links("http://www.biorxiv.org/content/early/recent?page=%d" % ipage)
    
    for ipapers in range(0,len(all_papers)-1):

        #try:
        
        #print("Browsing through paper #%d ..." % (ipapers+1))

        url = "http://www.biorxiv.org" + all_papers[ipapers]['link'] + ".article-metrics"

        metrics = gm.get_metrics(url)
        if (metrics[0] == 'NA') and (metrics[1] == 'NA'):
            continue
        else:
            count = count + 1
            pass

        title = gm.get_title(url)

        url = scholar.get_scholar_link(title)

        # pretend to be human
        dummy = scholar.do_nonesense() 

        citations = scholar.get_citations(url) 

        sleep(random.randint(5,30))

        #df = pd.DataFrame(np.array([1,2,3])[np.newaxis],index=[1],
        #columns=['a','b','c'])      

        # write into text file
        data_to_write = open('biorxiv_metrics.txt','a')
        data_to_write.write('%d \t %d \t %d \t %d \t %d \t %d \t %d\n' % (ipage, metrics[2], metrics[0], metrics[1],metrics[3],metrics[4], citations))
        data_to_write.close()




