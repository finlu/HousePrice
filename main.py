from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    # process.crawl('beike_spider')
    process.crawl('anjuke_spider')
    process.start()
