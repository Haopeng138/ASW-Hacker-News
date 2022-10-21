import requests
from urllib.parse import urlparse
import math
import datetime

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

def diffTimeHour(tp):
    dt = datetime.datetime.now()
    t2d = datetime.datetime.fromtimestamp(tp)
    diff = dt - t2d
    hours = diff.seconds/3600
    return math.trunc(hours) 

def getTop30News():
    newslist = []
    idlist = getTop30()

    for id in idlist:
        try:
            url = "https://hacker-news.firebaseio.com/v0/item/"+str(id)+".json?print=pretty"
            re = requests.get(url=url)
            noticia = re.json()
            t = diffTimeHour(noticia["time"])
            tmp = {
                'title':noticia['title'],
                'url':noticia['url'],
                'descendants':noticia['descendants'],
                'time': t,
                'score':noticia['score'],
                'by':noticia['by']
            }
            
            
            # for key in noticia.keys():
            #     print(key)
            newslist.append(tmp)
        except:
            pass

    return newslist



getTop30News()
## Que necesito : title, url,descendants,time ,score,by 