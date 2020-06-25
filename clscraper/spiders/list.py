import re

from datetime import datetime
from scrapy import Request, Spider
from scrapy.loader import ItemLoader

from clscraper.items import HousingListing

class ListSpider(Spider):
    name = "listspider"
    allowed_domains = ["vancouver.craigslist.org"]

    def parse(self, response):
        for result in response.css(".result-row"):

            #get num bedrooms and floor area from housing div
            rooms = None
            floor_area = None
            floor_area_units = None
            housing = result.css(".result-meta .housing::text").get()
            if housing:
                housing = [val.strip() for val in housing.split("-")]
                for value in housing:
                    if re.match(r"[0-9]+br", value):
                        rooms = int(value.replace("br", ""))
                    elif value.endswith("ft"):
                        floor_area = value.replace("ft", "")
                        floor_area_units = "ft"
                    elif value.endswith("m"):
                        floor_area = value.replace("m", "")
                        floor_area_units = "m"
            if floor_area:
                floor_area = int(floor_area)

            location = result.css(".result-hood::text").get()
            if location:
                location = location.strip()
                # location looks like `(Vancouver)`. lets remove the parens
                location = location[1:] if location[0] == "(" else location
                location = location[:-1] if location[-1] == ")" else location
            currency = None
            for line in response.text.split("\n"):
                match = re.match(r'.*areaCountry = "(.*)".*', line)
                if match:
                    country = match.group(1)
                    if country.startswith("CA"):
                        currency = "CAD"
                    elif country.startswith("US"):
                        currency = "USD"
                
            price = result.css(".result-meta > .result-price::text").get()
            match = re.match(r".?([0-9]+).?", price)
            price = int(match.group(1))
            yield HousingListing(
                id=int(result.css(".result-title").attrib["data-id"]),
                url=result.css(".result-title").attrib["href"],
                title=result.css(".result-title::text").get(),
                price=price,
                price_currency=currency,
                bedrooms=rooms,
                floor_area=floor_area,
                floor_area_units=floor_area_units,
                location=[location],
                datetime_scraped=datetime.utcnow(),
                partial_scrape=True
            )
