import requests
from bs4 import BeautifulSoup
from random import uniform, choice
import csv
from time import sleep



def get_html(url, proxy=None):
    r = requests.get(url, proxies=proxy)
    return r.text

def write_csv(data):
    with open('abebook.csv', 'a', newline='') as f:
        order = ['isbn','name','author','about','publisher','link','quantity','price','rating','shiping']
        writer = csv.DictWriter(f,fieldnames=order, delimiter=';')
        writer.writerow(data)


def parse_data(html):
    soup = BeautifulSoup(html,'lxml')
    books = soup.find('div',class_='result-set').find_all('div', class_='cf result')
    for book in books:
        try:
            isbn = book.find('p', class_='isbn small').find('a').text.strip()
        except:
            isbn = ''
        try:
            name = book.find('meta', itemprop='name').get('content')
        except:
            name = ''
        try:
            author = book.find('meta', itemprop='author').get('content')
        except:
            author = ''
        try:
            about = book.find('meta', itemprop='about').get('content')
        except:
            about = ''
        try:
            publisher = book.find('meta', itemprop='publisher').get('content')
        except:
            publisher = ''
        try:
            link = 'https://www.abebooks.com'+book.find('a').get('href')
        except:
            link = ''
        try:
            quantity = book.find('p', id='quantity')
        except:
            quantity = ''
        try:
            price = book.find('div', class_='srp-item-price').text.strip()
        except:
            price = ''
        try:
            rating = book.find('p', class_='bookseller-rating small').find('img').get('alt')
        except:
            rating = ''
        try:
            shiping = book.find('span', class_='srp-item-price-shipping').text.strip()
        except:
            shiping = ''
        data = {'name': name,'isbn':isbn, 'link':link, 'author':author,'about':about,'price':price,'publisher':publisher,'rating':rating,'shiping':shiping, 'quantity':quantity}
        write_csv(data)



def main():
    #64
    url = 'https://www.abebooks.com/servlet/SearchResults?bsi={}&n=100121503&pt=book&sortby=0&vci=6670492'
    step = 1
    for i in range(64):
        sleep(uniform(3,5))
        print(i)
        urll = url.format(step)
        parse_data(get_html(urll))
        step = step+30


if __name__ == '__main__':
    main()