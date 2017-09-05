# get data
import get_metrics as gm
import get_scholar_citations as scholar
import numpy as np
import os
count = 0
inp = []

if os.path.isfile('biorxiv_metrics.txt'):
    while True:
        inp = input("Data already exists: (o)verwrite or (c)reate copy? ")
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

for ipage in range(0,1500):

    print("Browsing page %d ..." % ipage)

    all_papers = gm.get_paper_links("http://www.biorxiv.org/content/early/recent?page=%d" % ipage)

    for ipapers in range(0,len(all_papers)-1):

        print("Browsing through paper #%d ..." % (ipapers+1))

        url = "http://www.biorxiv.org" + all_papers[ipapers]['link'] + ".article-metrics"

        metrics = gm.get_metrics(url)

        #if metrics == 'NA':

        #    url = "http://www.biorxiv.org" + all_papers[ipapers]['link'] + ".article-metrics"
            
        #    metrics = gm.get_metrics(url)[1]

        if (metrics[0] == 'NA') and (metrics[1] == 'NA'):
            continue
        else:
            print("Information found!")
            count = count + 1
            pass

        title = gm.get_title(url)

        url = scholar.get_scholar_link(title)

        citations = scholar.get_citations(url)       

        # write into text file
        data_to_write = open('biorxiv_metrics.txt','a')
        data_to_write.write('%d \t %d \t %d \t %d \t %d\n' % (ipage, metrics[2], metrics[0], metrics[1], citations))
        data_to_write.close()        


