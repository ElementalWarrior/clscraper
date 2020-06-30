import logging
import re
import sys

from datetime import datetime
from scrapy import Request, Spider
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from urllib.parse import urljoin

from clscraper.items import HousingListing
from clscraper.models import Posting, session_scope

logger = logging.getLogger(__name__)

class ListSpider(Spider):
    name = "listspider"
    start_urls = ["https://vancouver.craigslist.org/d/apts-housing-for-rent/search/apa"]
    allowed_domains = ["vancouver.craigslist.org"]

    def __init__(self, *args, listing_type, number_of_pages_to_scrape=1, url=None, **kwargs):
        """

        :param listing_type: Listing type: IE motorcycle parts, photography, apts/housing, etc
        :param number_of_pages_to_scrape: Number of pages to scrape, -1 for unlimited
        :param url: url to scrape, set to use different listing pages
        """
        number_of_pages_to_scrape = int(number_of_pages_to_scrape)
        self.listing_type = listing_type
        self.number_of_pages_to_scrape = number_of_pages_to_scrape - 1 if number_of_pages_to_scrape > 0 else number_of_pages_to_scrape
        if url:
            self.start_urls = [url]
        assert self.listing_type, "Listing type not specified"
        super().__init__(*args, **kwargs)

    def parse(self, response: HtmlResponse):
        """Parse function that scrapes HousingListing items from craigslist list pages.

        Gets inserted into the db with partial_scrape=True. Then the posting spider will pull that list of paritial
        scrapes and fill out the rest of the posting.
        """
        listings = []
        
        # go through each listing row and build a list of listing items
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

            location = HousingListing.location_str_to_dict(result.css(".result-hood::text").get())
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
            listing = HousingListing(
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
                partial_scrape=True,
                listing_type=self.listing_type
            )
            listings.append(listing)

        # take the list of scraped items and compare them to the database for stored values
        ids = [listing["id"] for listing in listings]
        with session_scope() as session:
            ids = [row[0] for row in session.query(Posting.id).filter(Posting.id.in_(ids)).all()]
            for listing in listings:
                if listing["id"] not in ids:
                    yield listing
                else:
                    logging.debug(f"Found an already scraped listing id={listing['id']}")

        # we pass along number of pages to scrape by using meta, if meta is not defined 
        if "number_of_pages_to_scrape" in response.meta:
            number_of_pages_to_scrape = response.meta.get("number_of_pages_to_scrape", None)
        else:
            number_of_pages_to_scrape = self.number_of_pages_to_scrape

        # if we configured it, scrape X pages
        next_anchor = response.css("a.next.button")
        if (number_of_pages_to_scrape or number_of_pages_to_scrape == -1) and next_anchor:
            url = urljoin(response.url, next_anchor.attrib["href"])
            yield Request(url, meta=dict(
                number_of_pages_to_scrape=number_of_pages_to_scrape-1 if number_of_pages_to_scrape != -1 else number_of_pages_to_scrape
            ))
