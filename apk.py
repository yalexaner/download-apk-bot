# coding=utf-8

import re
import requests
import shutil

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

class Apk(object):
    def find(self, url):
        url = re.sub(r'play\.google', 'apkpure', url)

        page = requests.get(url).text

        url = 'https://apkpure.com' + BeautifulSoup(page).body.find('a', attrs={'class': 'da'}).get('href')

        page = requests.get(url).text

        return BeautifulSoup(page).body.find('a', attrs={'id': 'download_link'}).get('href')

    def download(self, url):
        file = requests.get(self.find(url), stream = True)

        with open('file.apk', "wb") as receive:
                shutil.copyfileobj(file.raw, receive)
        
        del file
