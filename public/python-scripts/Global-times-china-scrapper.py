import requests
from bs4 import BeautifulSoup

import json
from datetime import date
# TO scrape data from globlatimes: https://www.globaltimes.cn/world/Top-News.html and retrieve data of day

today = date.today().strftime('%d')

# url = 'http://www.globaltimes.cn/'
url = 'https://www.globaltimes.cn/world/Top-News.html'

def getParsedHtml():
    print(url)
    rawData = requests.get(url)
    if(rawData.status_code == 200):
        soup = BeautifulSoup(rawData.content, 'html.parser')
        rawData.close()
        return soup
    else:
        return -1



def getNews(soup):

    articles = soup.select('div.span10')

    articleTitle = [article.select_one('h4 > a').getText() for article in articles]
    articleLink = [article.select_one('h4 > a').get('href') for article in articles]
    articleContent = [article.select_one('p').getText() for article in articles]
    article_date_source = [article.select_one('p > smaill').getText().split('|') for article in articles]



    l = len(articleTitle)
    print('total links found: ', l)
    newsList = []

    for i in range(l):
        news_date = article_date_source[i][1].split(' ')[1]
        newsList.append({'title': articleTitle[i], 'title-link': articleLink[i], 'content': articleContent[i], 'source': article_date_source[i][0], 'date': news_date})
    
    
    return newsList
    

def createJson(filename, newsDict):
    f = open(filename, 'w')
    json.dump(newsDict, f, indent=4, sort_keys= True)
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


def main():
    htmlParsed = getParsedHtml()
    if(htmlParsed != -1):
        news = getNews(htmlParsed)
        news = listToDict(news, 'date')
        createJson('public/data/global-times.json', news)

    else:
        print("error occured")
        return -1


main()