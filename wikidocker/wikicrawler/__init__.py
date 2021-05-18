import requests
from bs4 import BeautifulSoup
import re


class WikiCrawler:
    base_link = "https://simple.wikipedia.org"

    @staticmethod
    def __site_exist(url: str):
        """Verifies if given URL is valid"""
        request = requests.get(url)

        if request.status_code == 200:
            return True

        print("Site does not exist! [" + url + "]")
        return False

    def get_content(self, url):
        if not self.__site_exist(url):
            return None

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        soup = soup.find(id='content')

        text = soup.get_text()
        text = text.split('\nRelated pages', 1)[0]
        text = re.sub('(Jump to navigation|Jump to search)', '', text)
        text = re.sub('[^a-zA-Z]+', ' ', text)
        text = text.split()
        text = [word.lower() for word in text]

        return text

    def get_links_from_category(self, category):
        url = self.base_link + "/wiki/Category:" + category

        if not self.__site_exist(url):
            return None

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        soup = soup.find(id='mw-pages')
        soup = soup.find_all('a', href=True)

        links = []
        for link in soup:
            links.append(self.base_link + link['href'])

        return links

    def get_data(self):
        return None