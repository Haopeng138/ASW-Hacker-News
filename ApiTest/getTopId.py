import requests
from urllib.parse import urlparse
import json 

def getTopIds():
  respon = requests.get(url="https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")
  return respon.json()

def getTop30():
  topIds = getTopIds()
  idlist = []
  for index,id  in enumerate(topIds,start=1):
      if index == 31:
          break
      idlist.append(id)
  return idlist

def getDomain(url):
    domain = urlparse(url).netloc
    return str(domain)

def getTop30News():
    newslist = []
    idlist = getTop30()

    for id in idlist:
        url = "https://hacker-news.firebaseio.com/v0/item/"+str(id)+".json?print=pretty"
        re = requests.get(url=url)
        noticia = re.json()
        
        tmp = {
            'title':noticia['title'],
            'url':noticia['url'],
            'descendants':noticia['descendants'],
            'time':
        }
        
        # for key in noticia.keys():
        #     print(key)
        newslist.append(noticia)

    return 1


## Que necesito : title, url,descendants,time ,score,by 