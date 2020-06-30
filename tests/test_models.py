from clscraper.models import session_scope

def test_connection():
    with session_scope() as session:
        assert list(session.execute("select 1"))[0][0] == 1

def test_posting_revision():
    from datetime import datetime
    from clscraper.models import Posting, PostingRevision
    with session_scope() as session:
        kwargs = dict(
            title="Testing",
            url="Testing",
            partial_scrape=True,
            datetime_scraped=datetime.utcnow(),
            listing_type="apa",
        )
        posting = Posting(id=1, **kwargs)
        one = PostingRevision(id=1, posting_id=posting.id, **kwargs)
        two = PostingRevision(id=one.id+1, posting_id=posting.id, **kwargs)
        session.add(posting)
        session.flush()
        session.add(one)
        session.add(two)
        session.flush()
        assert one.id == 1
        assert two.id == 2