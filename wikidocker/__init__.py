import wikicrawler
import qualifier

if __name__ == '__main__':
    crawler = wikicrawler.WikiCrawler()
    #data = crawler.get_data(True)
    crawler.get_data_custom_site('https://www.vaticannews.va/en/pope/news/2021-05/pope-regina-coeli-pentecost-sunday-catechesis.html')

    qualifier = qualifier.Qualifier()
    qualifier.qualify_test_set()
    # qualifier.qualify_article_from_console()
    qualifier.qualify_article_from_file('custom_dump.json')
