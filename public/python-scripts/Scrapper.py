import requests
from bs4 import BeautifulSoup

import json

url = "https://timesofindia.indiatimes.com"

def getParsedHtml():
    print(url)
    rawData = requests.get(url)
    if(rawData.status_code == 200):
        soup = BeautifulSoup(rawData.content, 'html.parser')
        rawData.close()
        return soup
    else:
        return -1


def getTOINews(soup):
    links = list(soup.findAll('a'))
    print('total links found: ', len(links))
    newsList = []
    for link in links:
        attr = link.attrs
        if('title' in attr):
            newsList.append({'title': attr['title'], 'href': attr['href']})
    print('total news links found: ', len(newsList))
    return newsList


def cleanData(news):

    for item in news:
        link = item['href']
        if(link[0] == '/'):
            item['href'] = url + link

    # removes duplicate
    news = {frozenset(item.items()):item for item in news}.values()

    return news


def classifyNewsFromLink(articleLink):
    newsByTopic = {}
    for item in articleLink:
        link = list(item['href'].split('/'))
        if(link[0] == 'https:'):

            if link[2] in newsByTopic:
                newsByTopic[link[2]].append(item)
            else:
                newsByTopic[link[2]] = [item]

    return newsByTopic


def listToDict(newsList, pos):
    newDict = {}
    for item in newsList:
        link = item['href'].split('/')[pos]

        if link in newDict:
            newDict[link].append(item)
        else:
            newDict[link] = [item]

    return newDict


def classifyTOINewsByTopic(news):
    return listToDict(news, 3)


def createJson(filename, newsDict):
    f = open(filename, 'w')
    json.dump(newsDict, f, indent=4)
    f.close()
    print("News in file {0}".format(filename) )


def formatData(news):

    newsByTopic = classifyNewsFromLink(news)
    newsByTopic['timesofindia.indiatimes.com'] = classifyTOINewsByTopic(newsByTopic['timesofindia.indiatimes.com'])
    

    topicList = ['world', 'sports', 'city', 'entertainment', 'home', 'elections']
    for topic in topicList:
        newsByTopic['timesofindia.indiatimes.com'][topic] = listToDict(newsByTopic['timesofindia.indiatimes.com'][topic], 4)

    createJson('public/data/ToiNews.json', newsByTopic)

    return newsByTopic


def scrapper():
    htmlParsed = getParsedHtml()
    
    if(htmlParsed != -1):
        news = getTOINews(htmlParsed)
        news = cleanData(news)

        news = formatData(news)

    else:
        print("error occured")
        return -1


if __name__ == "__main__":
    scrapper = scrapper()

