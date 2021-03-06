import scrapy

class HousingListing(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field()
    price_currency = scrapy.Field()
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
    datetime_post_expires = scrapy.Field()
    listing_type = scrapy.Field()

    @staticmethod
    def location_str_to_dict(str):
        return f'{{"type":"string","value":"{str}"}}'