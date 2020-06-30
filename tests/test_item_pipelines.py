from datetime import datetime
from unittest.mock import patch

from clscraper.models import PostingRevision, session_scope
from clscraper.item_pipelines import PostgresPipeline
from clscraper.spiders.posting import PostingSpider

def test_posting(data_to_resp):
    url = "https://vancouver.craigslist.org/rds/reb/d/surrey-hottest-deal-of-the-week-5-bed-4/7147938227.html"
    path = "posting_realty_20200624.html"
    listing_type = "apa"
    response = data_to_resp(url, path, listing_type="apa")
    now = datetime.utcnow()
    with patch("clscraper.spiders.posting.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value = now
        spider = PostingSpider()
        item = next(spider.parse(response))
        PostgresPipeline().process_item(item, spider)
        PostgresPipeline().process_item(item, spider)
        PostgresPipeline().process_item(item, spider)
        PostgresPipeline().process_item(item, spider)
        with session_scope() as session:
            assert max(session.query(PostingRevision.id))[0] == 4
