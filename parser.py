import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

HOST = 'https://www.facebook.com'
URL = 'https://www.olx.ua/kiev/q-airdots/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}
CSV = 'blocks.csv'


# functions

def get_html(url, params=''):
    """Gets html code"""
    r = requests.get(url, headers = HEADERS, params=params) # making request to the page
    return r

def get_content(html):
    """Getting the block that we want to parse and getting the data from it"""
    soup = BeautifulSoup(html, 'html.parser') # getting the data
        
    # then finding all blocks that we need (with particular div class)
    items = soup.find_all('div', class_='offer-wrapper')
    blocks = [] #list for our items


    # making dictionary for a block and appending it to the 'blocks' list
    for item in items: 
        blocks.append(
            {
                'Title': item.find('div', class_='space rel').find('strong').get_text(strip=True),
                'Price': item.find('div', class_='space inlblk rel').find('p', class_='price').get_text(strip=True),
                'Link': item.find('div', class_='space rel').find('a').get('href'),
                'Image': item.find('td').find('img').get('src')
            }
        )

    return blocks

def save_data(items, path):
    with open(path, 'w', newline='') as data_file:
        writer = csv.writer(data_file, delimiter=',')
        writer.writerow(['Title', 'Price', 'Link', 'Image'])
        for item in items:
            writer.writerow([item['Title'], item['Price'], item['Link'], item['Image']])


def parser():
    """Parsing multiple pages"""
    PAGENATION = input('How many pages do you want to parse?')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        blocks = []
        for page in range(0, PAGENATION):
            print('\nParsing page number {page}'.format(page=page))
            html = get_html(URL, params={'page': page})
            blocks.extend(get_content(html.text))
            save_data(blocks, CSV)
    else:
        print('Something went wrong...')

parser()
