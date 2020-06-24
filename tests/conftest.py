import pytest

@pytest.fixture()
def load_data():
    def _(path):
        f = open(f"tests/data/{path}", "r")
        data = f.read()
        f.close()
        return data
    return _