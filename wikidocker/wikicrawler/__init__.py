import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import json


class WikiCrawler:
    base_link = "https://simple.wikipedia.org"

    @staticmethod
    def __site_exist(url: str):
        """Verifies if given URL is valid"""
        request = requests.get(url)

        if request.status_code == 200:
            return True

        raise Exception("Website return " + str(request.status_code))

    @staticmethod
    def __clean_article(article):
        with open("./wikicrawler/redundant_terms.json") as file:
            redundant_terms = json.load(file)
        file.close()

        article = article.split()

        for lemma in redundant_terms:
            article = list(filter(lambda x: x not in list(lemma.values())[0], article))

        return ' '.join(article)

    def __format_content(self, soup):
        soup = soup.find_all('p')

        text = ""
        for paragraph in soup:
            paragraph = paragraph.get_text().lower()
            paragraph = re.sub('[^a-zA-Z]+', ' ', paragraph)
            paragraph = " ".join(paragraph.split())
            text = "{0} {1}".format(text, paragraph)

        return self.__clean_article(text)

    def get_content(self, url):
        if not self.__site_exist(url):
            return None

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        soup = soup.find(id='content')

        return self.__format_content(soup)

    def get_links_from_category(self, category):
        url = self.base_link + "/wiki/Category:" + category

        if not self.__site_exist(url):
            return None

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        soup = soup.find(id='mw-pages')
        if soup is None:
            return None

        soup = soup.find_all('a', href=True)

        links = []
        for link in soup:
            links.append(self.base_link + link['href'])

        return links

    @staticmethod
    def __get_existing_category(category):
        word = category.lower()
        if word == 'farming':
            return 'Farms'
        elif word == 'industry':
            return 'Industries'
        elif word == 'custom':
            return 'Traditions'
        elif word == 'book':
            return 'Books'
        elif word == 'movies and films':
            return 'Movies'
        elif word == 'earth science':
            return 'Earth sciences'
        elif word == 'laws':
            return 'Legislation'

        return category

    def get_data(self, serialize=False):
        url = "https://simple.wikipedia.org/wiki/Main_Page"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        soup = soup.find(id='mf-know')
        soup = soup.find('tbody')
        soup = soup.find_all('td', style=None)

        data = []

        for tag in soup:
            title = tag.find('b')
            if title is None:
                continue

            title = title.text
            categories = tag.find_all('a')
            category_data = {'category': title, 'subcategories': []}
            print(title + ":")

            for category in categories:
                category = category.text
                category = self.__get_existing_category(category)

                category_links = self.get_links_from_category(category)

                if category_links is None:
                    print(category + ": Category does not exist! Skipping...")
                    continue

                subcategory_data = {'name': category, 'articles': []}

                for link in tqdm(category_links, desc=category):
                    article = self.get_content(link)

                    subcategory_data['articles'].append(article)

                category_data['subcategories'].append(subcategory_data)

            data.append(category_data)
            print()

        if serialize:
            with open("../wiki_dump.json", "w") as file:
                json.dump(data, file)
            file.close()

        return data

    def get_content_custom_site(self, url):
        """gets article by getting content of all <p> tags from website"""
        if not self.__site_exist(url):
            return None

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        return self.__format_content(soup)

    def get_data_custom_site(self, url):
        """serialize and returns article from custom website"""
        data = self.get_content_custom_site(url)

        with open("data_to_qualify/custom_dump.json", "w") as file:
            json.dump(data, file)
        file.close()

        return data
