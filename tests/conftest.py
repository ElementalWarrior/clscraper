import logging
import pytest
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
    def _(url, path):
        body = load_data(path)
        response = HtmlResponse(url, body=body.encode("utf-8"))
        return response
    return _

@pytest.fixture(autouse=True)
def db():
    from clscraper.models import DeclarativeBase, engine
    DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)