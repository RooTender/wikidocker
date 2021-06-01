import wikicrawler
import qualifier
import trainer

if __name__ == '__main__':
    crawler = wikicrawler.WikiCrawler()

    input_data = input('Enter site to qualify: ')
    crawler.get_data_custom_site(input_data)

    qualifier = qualifier.Qualifier()
    qualifier.qualify_article_from_file('custom_dump.json')
