import requests
from collections import Counter

dois = ['10.1038/ncomms13526', '10.1038/s41593-018-0122-4', 
    '10.1371/journal.pcbi.1005171', '10.3389/fnsys.2016.00037', 
  '10.7554/eLife.11946', '10.1002/hbm.22466','10.1371/journal.pcbi.1003854']#
     #,'10.1111/j.1469-8986.2011.01226.x']

auth_list = []

for i in range(0,len(dois)):

    print(i)

    url = 'http://api.crossref.org/works/' + dois[i]

    req = requests.get(url).json()['message']['reference']

    for j in range(0,len(req)):
        
        if 'DOI' in req[j].keys():
            url2 = 'http://api.crossref.org/works/' + req[j]['DOI']
            req2 = requests.get(url2).json()['message']
            auth = req2['author']
        else:
            continue

        for k in range(0,len(auth)):

            auth_list.append(auth[k]['family']+auth[k]['given'][0])

    counts = Counter(auth_list)
    print(counts)

print("Final count")

counts = Counter(auth_list)
print(counts)




