import requests
from bs4 import BeautifulSoup

import json

url = 'https://www.usatoday.com/'

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

    newsList = []
    articles = soup.select('a.gnt_m_th_a')

    articleTitle = [article.getText() for article in articles]
    articleLink = [article.get('href') for article in articles]

    # print(articleTitle)
    # print('====================================================================\n\n')
    # print(articleLink)
    # print('====================================================================\n\n')

    l = len(articleTitle)
    print('total links found: ', l)

    for i in range(l):
        
        newsList.append({'title': articleTitle[i], 'link': articleLink[i] })
    

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



def cleanData(newsList):

    for article in newsList:

    # adds parent link if not present
        if article['link'][0] == '/':
            article['link'] = url + article['link']

    return newsList


def main():
    htmlParsed = getParsedHtml()
    if(htmlParsed != -1):
        news = getNews(htmlParsed)

        news = cleanData(news)
        createJson('public/data/usa-today.json', {'top-news': news})

    else:
        print("error occured")
        return -1


main()