import requests
from bs4 import BeautifulSoup


class WikiCrawler:
    @staticmethod
    def __site_exist(url: str):
        """Verifies if given URL is valid"""
        request = requests.get(url)

        if request.status_code == 200:
            return True

        print("Site does not exist! [" + url + "]")
        return False

    def extract_links_from_category(self, category):
        url = "https://simple.wikipedia.org/wiki/Category:" + category

        if not self.__site_exist(url):
            return None

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        soup = soup.find(id='mw-pages')
        soup = soup.find_all('a', href=True)

        links = []
        for link in soup:
            links.append("https://simple.wikipedia.org" + link['href'])

        return links

    # def get_categories_articles(self):
