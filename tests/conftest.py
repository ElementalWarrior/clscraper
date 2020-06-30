import logging
import pytest
from scrapy import Request
from scrapy.http import HtmlResponse

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture()
def load_data():
    def _(path):
        f = open(f"tests/data/{path}", "r")
        data = f.read()
        f.close()
        return data
    return _

@pytest.fixture()
def data_to_resp(load_data):
    def _(url, path, listing_type):
        body = load_data(path)
        response = HtmlResponse(url, body=body.encode("utf-8"), request=Request(url, meta=dict(
            number_of_pages_to_scrape=-1,
            listing_type=listing_type,
        )))
        return response
    return _

@pytest.fixture(autouse=True)
def db():
    from clscraper.models import DeclarativeBase, engine
    DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)