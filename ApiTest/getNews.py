import requests

id = 8863
url = "https://hacker-news.firebaseio.com/v0/item/"+str(id)+".json?print=pretty"
re = requests.get(url=url)

noticia = re.json()


# for key in noticia.keys():
#     print(key)

for value in noticia:
    print(noticia[str(value)])