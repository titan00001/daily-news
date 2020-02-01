import requests
from bs4 import BeautifulSoup

import re
import json
from datetime import datetime

url = "https://www.moneycontrol.com/news/news-all/"
filename = "public/data/money-control-economic.json"


def getParsedHtml(url):
    print(url)
    rawData = requests.get(url)
    if(rawData.status_code == 200):
        soup = BeautifulSoup(rawData.content, 'html.parser')
        rawData.close()
        return soup
    else:
        return -1

# more news : li.clearfix > span
# li.clearfix > h2 > a
# li.clearfix > p


def getNews(soup):

    newsList = []
    articles = soup.select('li.clearfix')


    titles = [article.select_one('h2 > a').getText() for article in articles]
    links = [article.select_one('h2 > a').get('href') for article in articles]
    # topics = [article.select_one('span.program-name').getText() if article.select_one('span.program-name') else "" for article in articles]
    contents = [article.select_one('p').getText() if article.select_one('p') else "" for article in articles]
    dates = [article.select_one('span').getText() if article.select_one('span') else "" for article in articles]

    # f = open('moneyControl.txt', 'w')
    # for article in articles:
    #     f.write(str(article))
    #     f.write('\n\n')
    # f.close()

    l = len(titles)
    print('total links found: ', l)

    for i in range(l):
        
        newsList.append({'title': titles[i], 'link': links[i], 'content': contents[i], 'date': dates[i].split(',')[0] })
    
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

def nextPage(soup):

    ''' For Scrolling to next page: customized for money-Control'''
    next_page_link = soup.select_one('a.last').get('href')

    if next_page_link[0] != 'h':

        next_page_link = 'https://www.moneycontrol.com/' + next_page_link

    soup = getParsedHtml(next_page_link)
    return soup


def main():

    today = datetime.now().strftime('%d')
    last_news_date = today

    newsList = []
    htmlParsedSoup = getParsedHtml(url)
    page = 0

    while(today == last_news_date):

        if(htmlParsedSoup != -1):

            news = getNews(htmlParsedSoup)

            last_news_date = news[-1]['date'].split(' ')[-1]

            newsList = newsList + news

            htmlParsedSoup = nextPage(htmlParsedSoup)

            page = page + 1

        else:
            print("error occured")
            break

    news = cleanData(newsList)

    news = {'economic': news}

    createJson(filename, news)

    


main()