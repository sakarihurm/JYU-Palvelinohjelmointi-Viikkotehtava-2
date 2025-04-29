import pytest
try:
  import vt2
except:
  try:
      import oma as vt2
  except:
      import app as vt2

@pytest.fixture()
def app():
    app = vt2.app
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
