import requests
from bs4 import BeautifulSoup

import re
import json

url = "https://www.euronews.com/european-affairs/european-news"

def getParsedHtml():
    print(url)
    rawData = requests.get(url)
    if(rawData.status_code == 200):
        soup = BeautifulSoup(rawData.content, 'html.parser')
        rawData.close()
        return soup
    else:
        return -1

# more news : div.o-block-more-news-themes__articles > 


def getNews(soup):

    newsList = []
    articles = soup.select('div.m-object__body')


    titles = [article.select_one('a.m-object__title__link').getText() for article in articles]
    links = [article.select_one('a.m-object__title__link').get('href') for article in articles]
    topics = [article.select_one('span.program-name').getText() if article.select_one('span.program-name') else "" for article in articles]
    contents = [article.select_one('a.m-object__description__link > p').getText() if article.select_one('a.m-object__description__link > p') else "" for article in articles]
    dates = [article.select_one('div.m-object__publishedAt > time').getText() if article.select_one('div.m-object__publishedAt > time') else "" for article in articles]


    l = len(titles)
    print('total links found: ', l)

    for i in range(l):
        
        newsList.append({'title': titles[i], 'link': links[i], 'topic': topics[i], 'content': contents[i], 'date': dates[i] })
    
    return newsList
    

def createJson(filename, newsDict):
    f = open(filename, 'w')
    json.dump(newsDict, f, indent=4)
    f.close()
    print("News in file {0}".format(filename) )


def listToDict(newsList, topic):
    newDict = {}
    for item in newsList:

        key = item[topic]

        if key in newDict:
            newDict[key].append(item)
        else:
            newDict[key] = [item]

    return newDict


def cleanData(newsList):
    
    url = 'https://www.euronews.com'

    for article in newsList:

    # removes whitespace and escape character
        for key in article:
            article[key].replace('\n',' ')
            article[key] = article[key].strip()

    # adds parent link if not present
        if article['link'][0] == '/':
            article['link'] = url + article['link']
    
    # adds date if not present
        if article['date'] == '':
            date = article['link'].split('/')

            if 'video' == date[3]:
                article['date'] = date[6]+'/'+ date[5]+'/'+ date[4]
            else:
                article['date'] = date[5]+'/'+ date[4]+'/'+ date[3]


    print('Total links after cleanup: {0}'.format(len(newsList)))
    return newsList


def main():
    htmlParsed = getParsedHtml()
    if(htmlParsed != -1):
        news = getNews(htmlParsed)

        news = cleanData(news)

        news = listToDict(news, 'topic')
        createJson('public/data/european-news.json', news)

    else:
        print("error occured")
        return -1


main()