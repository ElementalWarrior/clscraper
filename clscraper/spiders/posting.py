import logging
import re
import scrapy
from time import sleep

from datetime import datetime
from dateutil.parser import parse as datetime_parse
from lxml.html.soupparser import fromstring
from lxml.html import tostring

from clscraper.items import HousingListing
from clscraper.models import Posting, session_scope

logger = logging.getLogger(__name__)


class PostingSpider(scrapy.Spider):
    name = "postingspider"
    allowed_domains = ["vancouver.craigslist.org"]

    def start_requests(self):
        with session_scope() as session:
            for posting in session.query(Posting).filter(Posting.partial_scrape).all():
                yield scrapy.Request(posting.url, meta=dict(
                    listing_type=posting.listing_type
                ))

    def parse_neighborhood(self, response):
        value = response.css(".postingtitletext > small::text").get()
        if value:
            value = value.strip()
            # location looks like `(Vancouver)`. lets remove the parens
            value = value[1:] if value[0] == "(" else value
            value = value[:-1] if value[-1] == ")" else value
            return value

    def parse_price(self, response):
        price = response.css(".price::text").get()
        if not price:
            return
        price = price.replace(",", "")
        # it appears price must be an integer
        match = re.match(r".?([0-9]+).?", price)
        return int(match.group(1))

    def parse_rooms(self, response):
        value = response.css(".housing::text").get()

        if value:
            value = value.replace("/", "")
            parts = [v.strip() for v in value.split("-")]
            rooms = None
            for p in parts:
                if re.match(r"[0-9]+br", p):
                    rooms = int(p.replace("br", ""))
                    break
            return rooms

    def parse_baths(self, response):
        attribs = response.css(".attrgroup .shared-line-bubble b::text")

        # go through each bubble
        for a in attribs:
            text = a.get().lower().strip()

            # search a bold tag with format 2ba
            if re.match(r"[0-9]+ba", text):
                return int(text.replace("ba", ""))

    def parse_floor_area(self, response):
        value = response.css(".housing::text").get()
        if value:
            value = value.replace("/", "")
            parts = [v.strip() for v in value.split("-")]
            baths = None
            units = None
            for p in parts:
                if re.match(r"[0-9]+ft", p):
                    baths = int(p.replace("ft", ""))
                    units = "ft"
                    break
                if re.match(r"[0-9]+m", p):
                    baths = int(p.replace("m", ""))
                    units = "m"
                    break
            return baths, units
        return None, None

    def parse_description(self, response):

        desc = response.xpath('//*[@id="postingbody"]').extract_first()

        # lxml fromstring injects html tags for some reason
        xml = fromstring(desc)
        xml = xml.get_element_by_id("postingbody")

        innerHtml = ""
        for child in xml.xpath("/html/section/node()"):
            if not isinstance(child, str):
                innerHtml += tostring(child, encoding="unicode")

        return innerHtml

    def parse_images(self, response):
        imgs = [img.attrib["href"] for img in response.css("#thumbs a")]
        return imgs

    def parse_title(self, response):
        title = response.css("#titletextonly::text").get()
        return title

    def parse_mapaddress(self, response):
        return response.css(".mapaddress::text").get()

    def parse_id(self, response):
        for postinfo in response.css(".postinginfo::text"):
            text = postinfo.get()
            if re.match(r"post id:.*", text):
                return int(text.replace("post id: ", ""))

    def parse_posted(self, response):
        return response.css("#display-date .date").attrib["datetime"]

    def parse_map(self, response):
        map_ = response.css("#map")
        if map_:
            return {
                "type": "radix",
                "latitude": map_.attrib["data-latitude"],
                "longitude": map_.attrib["data-longitude"],
                "accuracy": map_.attrib["data-accuracy"],
            }

    def parse_url(self, response):
        return response.url

    def parse_georegion(self, response):
        meta = response.xpath('//meta[@name="geo.region"]')
        if meta:
            return meta.attrib["content"]

    def parse_post_expires(self, response):
        meta = response.xpath('//meta[@name="robots"]')
        if meta:
            for robot_param in meta.attrib["content"].split(","):
                if robot_param.startswith("unavailable_after"):
                    dt = robot_param.replace("unavailable_after: ", "")
                    return datetime_parse(dt)


    def parse(self, response):
        if response.css(".removed"):
            id = int(re.match(r".*\/([0-9]+)\.html", response.url).group(1))
            yield HousingListing(id=id, partial_scrape=False, url=response.url, datetime_scraped=datetime.utcnow())
            return

        georegion = self.parse_georegion(response)
        currency = None
        if georegion:
            currency = None
            if georegion.startswith("CA"):
                currency = "CAD"
            elif georegion.startswith("US"):
                currency = "USD"
        location_strs = [HousingListing.location_str_to_dict(str) for str in [
            self.parse_neighborhood(response),
            self.parse_mapaddress(response),
            georegion,
        ]]
        locations = location_strs + [
            self.parse_map(response),
        ]
        locations = [l for l in locations if l]
        floor_area, floor_units = self.parse_floor_area(response)
        kwargs = dict(
            id=self.parse_id(response),
            url=self.parse_url(response),
            datetime_posted=self.parse_posted(response),
            location=locations,
            bedrooms=self.parse_rooms(response),
            bathrooms=self.parse_baths(response),
            floor_area=floor_area,
            floor_area_units=floor_units,
            price=self.parse_price(response),
            price_currency=currency,
            description=self.parse_description(response),
            images=self.parse_images(response),
            title=self.parse_title(response),
            datetime_post_expires=self.parse_post_expires(response),
            partial_scrape=False,
            datetime_scraped=datetime.utcnow(),
            listing_type=response.meta["listing_type"]
        )
        yield HousingListing(**kwargs)
