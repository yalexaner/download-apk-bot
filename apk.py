# coding=utf-8

import re
import requests
import shutil
from bs4 import BeautifulSoup

class Apk(object):
    def name(self, url):
        url = re.sub(r'play\.google', 'apkpure', url)

        page = requests.get(url).text

        return BeautifulSoup(page).body.find('div', attrs={'class': 'title-like'}).text.strip()

    def find(self, url):
        url = re.sub(r'play\.google', 'apkpure', url)

        page = requests.get(url).text

        url = 'https://apkpure.com' + BeautifulSoup(page).body.find('a', attrs={'class': 'da'}).get('href')

        page = requests.get(url).text

        return BeautifulSoup(page).body.find('a', attrs={'id': 'download_link'}).get('href')

    def download(self, url):
        try:
            return requests.get(self.find(url), stream=True).content
        except AttributeError:
            return ''
