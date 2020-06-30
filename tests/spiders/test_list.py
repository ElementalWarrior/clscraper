from datetime import datetime
from scrapy import Item
from unittest.mock import patch

from clscraper.spiders.list import ListSpider

def test_parse(data_to_resp):
    now = datetime.utcnow()
    url = "http://vancouver.craigslist.example.com"
    path = "list_response_20200623.html"
    listing_type = "apa"
    response = data_to_resp(url, path, listing_type)
    with patch("clscraper.spiders.list.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value = now
        results = ListSpider(listing_type=listing_type).parse(response)
        for res in results:
            # dont assert on the yield Request(...) results
            if not isinstance(res, Item):
                continue
            assert res["datetime_scraped"] == now
            assert res["partial_scrape"]
            assert res["price_currency"] == "CAD"
            assert isinstance(res["price"], int)
            assert isinstance(res["title"], str)
            assert isinstance(res["url"], str)
            assert isinstance(res["id"], int)
            if res.get("bedrooms", None):
                assert isinstance(res["bedrooms"], int)
            if res.get("floor_area", None):
                assert isinstance(res["floor_area"], int)
            assert len(res["location"]) > 0

def test_parse_realty(data_to_resp):
    now = datetime.utcnow()
    url = "http://vancouver.craigslist.example.com"
    path = "list_realty_response_20200624.html"
    listing_type = "rea"
    response = data_to_resp(url, path, listing_type)
    with patch("clscraper.spiders.list.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value = now
        results = ListSpider(listing_type=listing_type).parse(response)
        for res in results:
            # dont assert on the yield Request(...) results
            if not isinstance(res, Item):
                continue
            assert res["datetime_scraped"] == now
            assert res["partial_scrape"]
            assert res["price_currency"] == "CAD"
            assert isinstance(res["price"], int)
            assert isinstance(res["title"], str)
            assert isinstance(res["url"], str)
            assert isinstance(res["id"], int)
            if res.get("bedrooms", None):
                assert isinstance(res["bedrooms"], int)
            if res.get("floor_area", None):
                assert isinstance(res["floor_area"], int)
            assert len(res["location"]) > 0