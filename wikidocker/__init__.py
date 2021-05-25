import wikicrawler

if __name__ == '__main__':
    crawler = wikicrawler.WikiCrawler()
    # data = crawler.get_data(True)

    my_data = crawler.get_data_custom_site('https://www.nytimes.com/live/2021/05/24/world/belarus-ryanair-protasevich')
