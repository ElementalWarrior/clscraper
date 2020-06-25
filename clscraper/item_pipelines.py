import logging
import scrapy
from sqlalchemy.sql.expression import func

from clscraper.models import Session
from clscraper.spiders import ListSpider, PostingSpider

from clscraper.models import Posting, PostingRevision

logger = logging.getLogger(__name__)

class PostgresPipeline:

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(spider, ListSpider):
            return
        session = Session()
        if isinstance(spider, PostingSpider):
            posting = session.query(Posting).filter(Posting.id == item["id"]).one_or_none()

            # upsert posting
            if posting:
                logger.debug(f"Updating {posting}")
                for column in Posting.__mapper__.columns:
                    if column.name != "id":
                        new_value = getattr(posting, column.name)
                        setattr(posting, column.name, new_value)
            else:
                posting = Posting(**item)
                session.add(posting)
                logger.debug(f"Creating {posting}")

            # get new revision_id and create posting revision
            kwargs = dict(**item)
            kwargs["posting_id"] = item["id"]
            max_id = (
                session.query(
                    func.coalesce(func.max(PostingRevision.id), 0)
                )
                .filter(PostingRevision.posting_id==item["id"])
                .one()[0]
            )
            kwargs["id"] = max_id+1
            revision = PostingRevision(**kwargs)
            logger.debug(f"Creating {revision}")
            session.add(revision)
            session.commit()

        return item