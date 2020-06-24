from clscraper.models import session_scope

def test_connection():
    with session_scope() as session:
        assert list(session.execute("select 1"))[0][0] == 1
