import pytest
from scrapy.http import HtmlResponse

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