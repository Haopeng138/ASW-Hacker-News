from django.http import HttpResponse
from django.template import loader
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
            dm = getDomain(noticia["url"])
            tmp = {
                'title':noticia['title'],
                'url':noticia['url'],
                'descendants':noticia['descendants'],
                'time': t,
                'score':noticia['score'],
                'by':noticia['by'],
                'domain':dm
            }
            
            
            # for key in noticia.keys():
            #     print(key)
            newslist.append(tmp)
        except:
            pass

    return newslist


def index(request):
  template = loader.get_template('homepage.html')
  newslist = getTop30News()
  context = {
    'news' : newslist
  }
  return HttpResponse(template.render(context,request))

def login(request):
  template = loader.get_template('login.html')
  return HttpResponse(template.render())

def submit(request):
  return HttpResponse()