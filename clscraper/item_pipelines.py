import scrapy

from clscraper.models import Session
from clscraper.spiders import ListSpider, PostingSpider

class PostgresPipeline:

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(spider, ListSpider):
            return
        session = Session()
        if isinstance(spider, PostingSpider):
        
        return item