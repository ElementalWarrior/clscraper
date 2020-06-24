from scrapy.http import HtmlResponse

from clscraper.spiders.list import ListSpider

def test_parse(load_data):
    body = load_data("list_response_20200623.html")
    response = HtmlResponse("vancouver.craigslist.example.com", body=body.encode("utf-8"))
    results = ListSpider().parse(response)
    for res in results:
        print(res)