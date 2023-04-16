import requests
from bs4 import BeautifulSoup as BS

host = 'https://www.igromania.ru'


def news():
    '''Новости'''
    r = requests.get("https://www.igromania.ru/news/")
    soup = BS(r.content, 'lxml')
    data = soup.find_all(class_="aubl_item")
    news = []
    for item in data:
        inf = item.find(class_="aubli_img")
        title = inf.find("img").get("alt")
        dop = item.find(class_="aubli_desc").text
        ssylka = inf.get('href')
        news.append((title, dop, f'{host}{ssylka}'))
    return news


def games():
    '''Игры'''
    r = requests.get('https://www.igromania.ru/news/game/')
    soup = BS(r.content, 'lxml')
    data = soup.find_all(class_="aubl_item")
    games = []
    for item in data:
        inf = item.find(class_="aubli_img")
        title = inf.find("img").get("alt")
        dop = item.find(class_="aubli_desc").text
        ssylka = inf.get('href')
        games.append((title, dop, f'{host}{ssylka}'))
    return games


def cybersport():
    '''Киберспорт'''
    r = requests.get('https://www.igromania.ru/news/cybersport/')
    soup = BS(r.content, 'lxml')
    data = soup.find_all(class_="aubl_item")
    cyber = []
    for item in data:
        inf = item.find(class_="aubli_img")
        title = inf.find("img").get("alt")
        dop = item.find(class_="aubli_desc").text
        ssylka = inf.get('href')
        cyber.append((title, dop, f'{host}{ssylka}'))
    return cyber


def movie():
    '''Кино'''
    r = requests.get('https://www.igromania.ru/news/kino/')
    soup = BS(r.content, 'lxml')
    data = soup.find_all(class_="aubl_item")
    movie = []
    for item in data:
        inf = item.find(class_="aubli_img")
        title = inf.find("img").get("alt")
        dop = item.find(class_="aubli_desc").text
        ssylka = inf.get('href')
        movie.append((title, dop, f'{host}{ssylka}'))
    return movie


def electronics():
    '''Элктроника'''
    r = requests.get('https://www.igromania.ru/news/hard/')
    soup = BS(r.content, 'lxml')
    data = soup.find_all(class_="aubl_item")
    electr = []
    for item in data:
        inf = item.find(class_="aubli_img")
        title = inf.find("img").get("alt")
        dop = item.find(class_="aubli_desc").text
        ssylka = inf.get('href')
        electr.append((title, dop, f'{host}{ssylka}'))
    return electr


def discount():
    '''Скидки'''
    r = requests.get('https://www.igromania.ru/news/sale/')
    soup = BS(r.content, 'lxml')
    data = soup.find_all(class_="aubl_item")
    discount = []
    for item in data:
        inf = item.find(class_="aubli_img")
        title = inf.find("img").get("alt")
        dop = item.find(class_="aubli_desc").text
        ssylka = inf.get('href')
        discount.append((title, dop, f'{host}{ssylka}'))
    return discount

