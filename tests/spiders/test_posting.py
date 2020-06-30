from datetime import datetime
from unittest.mock import patch

from clscraper.items import HousingListing
from clscraper.spiders.posting import PostingSpider

def test_posting(data_to_resp):
    url = "https://vancouver.craigslist.org/van/apa/d/vancouver-living-in-hermitage-2-br/7146512696.html"
    path = "posting_20200624.html"
    listing_type = "apa"
    response = data_to_resp(url, path, listing_type)
    now = datetime.utcnow()
    with patch("clscraper.spiders.posting.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value = now
        results = PostingSpider().parse(response)
        for r in results:
            assert r["bedrooms"] == 2
            assert r["bathrooms"] == 2
            location_hints = [
                "Vancouver",
                "778 near Richard",
                "CA-BC",
            ]
            for l in location_hints:
                l = HousingListing.location_str_to_dict(l)
                assert l in r["location"]
            map_dict = None
            for l in r["location"]:
                if isinstance(l, dict):
                    map_dict = l
            assert map_dict.get("type") == "radix"

            assert r["images"]
            for src in r["images"]:
                assert "images.craigslist.org" in src

            assert r["title"] == "**Living in L' Hermitage 2 BR** (Yaletown)"

            assert r["id"] == 7146512696

            assert r["floor_area"] == 890
            assert r["floor_area_units"] == "ft"

            assert r["datetime_posted"] == "2020-06-22T13:26:58-0700"

            assert r["url"] == "https://vancouver.craigslist.org/van/apa/d/vancouver-living-in-hermitage-2-br/7146512696.html"

            assert r["datetime_scraped"] == now

            assert r["price"] == 3450
            assert r["price_currency"] == "CAD"
            assert r["listing_type"] == "apa"

def test_posting_realty(data_to_resp):
    url = "https://vancouver.craigslist.org/rds/reb/d/surrey-hottest-deal-of-the-week-5-bed-4/7147938227.html"
    path = "posting_realty_20200624.html"
    listing_type = "rea"
    response = data_to_resp(url, path, listing_type=listing_type)
    now = datetime.utcnow()
    with patch("clscraper.spiders.posting.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value = now
        results = PostingSpider().parse(response)
        for r in results:
            assert r["bedrooms"] is None
            assert r["bathrooms"] is None
            location_hints = [
                "SURREY",
                "13909 59A Ave",
                "CA-BC",
            ]
            for l in location_hints:
                l = HousingListing.location_str_to_dict(l)
                assert l in r["location"]
            map_dict = None
            for l in r["location"]:
                if isinstance(l, dict):
                    map_dict = l
            assert map_dict.get("type") == "radix"

            assert len(r["images"]) > 1
            for src in r["images"]:
                assert "images.craigslist.org" in src

            assert r["title"] == "HOTTEST DEAL OF THE WEEK! 5 BED 4 BATH LOVELY HOME! THIS WON'T LAST!"

            assert r["id"] == 7147938227

            assert r["datetime_posted"] == "2020-06-24T19:14:19-0700"

            assert r["url"] == "https://vancouver.craigslist.org/rds/reb/d/surrey-hottest-deal-of-the-week-5-bed-4/7147938227.html"

            assert r["datetime_scraped"] == now

            assert r["price"] is None
            assert r["price_currency"] == "CAD"
            assert r["listing_type"] == "rea"
