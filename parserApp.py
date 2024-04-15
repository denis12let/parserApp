import requests
import sys
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

file = "C:\python\LOT3\Vakancies.txt"
sys.setrecursionlimit(300000)
if (os.path.exists(file)):
    os.remove(file)

header = {'user-agent': 'ooopa'}


def servAnalytic(mainLink):
    with ThreadPoolExecutor() as executor:
        for i in range(2, 100):
            print('main:          ' + str(i))
            link = mainLink + str(i)
            executor.submit(servLinkProcess, link)


def servLinkProcess(link):
    html = exceptionHandler(link)

    soup = BeautifulSoup(html.text, 'lxml')
    data = soup.find('p').get_text().replace("[","").replace("]","").replace("\"", "").split(',')
    data = list(filter(lambda item: 'rabota.by' in item, data))

    getDataLink(data)


def getDataLink(data):
    with ThreadPoolExecutor() as executor:
        for link in data:
            print(link)
            executor.submit(vacancyLinkProcess, link)
  

def vacancyLinkProcess(link):
    html = exceptionHandler(link)

    if (html == False):
        return

    soup = BeautifulSoup(html.text, 'lxml')

    vacancyName = soup.find('h1', {'data-qa': 'vacancy-title'})
    vacancySalary = soup.find('div', {'data-qa': 'vacancy-salary'})
    vacancySmallDescription = soup.find_all('p', class_='vacancy-description-list-item')
    vacancyEmployerName = soup.find('a', {'data-qa': 'vacancy-company-name'})
    vacancyEmployerAdress = soup.find('a', {'data-qa': 'vacancy-view-link-location'})

    vacancyLiteData = {
        "vacancyName": vacancyName.text if vacancyName else None,
        "vacancySalary": vacancySalary.text if vacancySalary else 'Пока не знаю, но меньше, чем ты думаешь',
        "vacancySmallDescription": ' '.join([item.text for item in vacancySmallDescription]),
        "vacancyEmployerName": vacancyEmployerName.text if vacancyEmployerName else None,
        "vacancyEmployerAdress": vacancyEmployerAdress.text if vacancyEmployerAdress else None
    }

    with open("C:\python\LOT3\Vakancies.txt", "a") as file:
        file.write("\n\n/**************************/\n\n")
        for key, value in vacancyLiteData.items():
            file.write("{0}: {1}\n".format(key, value))
    


def exceptionHandler(link):
        try:
            return requests.get(link, headers=header)
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            return False


startLink = 'http://188.225.26.112:8000/run?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82?p='

servAnalytic(startLink)