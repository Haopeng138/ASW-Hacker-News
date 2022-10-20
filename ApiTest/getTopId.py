import requests

re = requests.get(url="https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")

topIds = re.json()

for id in topIds:
    print(id)