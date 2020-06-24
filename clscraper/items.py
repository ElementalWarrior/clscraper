import scrapy

class HousingListing(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    floor_area = scrapy.Field()
    floor_area_units = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    location = scrapy.Field()
    attributes = scrapy.Field()
    datetime_posted = scrapy.Field()
    pictures = scrapy.Field()
    partial_scrape = scrapy.Field()
    datetime_scraped = scrapy.Field()