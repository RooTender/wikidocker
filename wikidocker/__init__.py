import wikicrawler

if __name__ == '__main__':
    crawler = wikicrawler.WikiCrawler()
    links = crawler.extract_links_from_category("Architecture")
    x = 0
