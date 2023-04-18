import requests
from bs4 import BeautifulSoup as BS

host = 'https://www.igromania.ru'


def get_info(link):
    r = requests.get(link)
    soup = BS(r.content, 'lxml')
    data = soup.find_all(class_="aubl_item")
    info = []
    for item in data:
        inf = item.find(class_="aubli_img")
        title = inf.find("img").get("alt")
        dop = item.find(class_="aubli_desc").text
        ss = inf.get('href')
        info.append((title, dop, f'{host}{ss}'))
    return info
