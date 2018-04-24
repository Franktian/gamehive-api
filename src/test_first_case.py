import pytest
from .app import *

def capital_case(x):
    print("Frank is testing")
    return x.capitalize()

def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'

@pytest.fixture
def client(request):
    test_client = app.test_client()

    def teardown():
        pass # databases and resourses have to be freed at the end. But so far we don't have anything

    request.addfinalizer(teardown)
    return test_client

def test_dummy(client):
    response = client.get('/')
    assert b'Game Hive Player API' in response.data