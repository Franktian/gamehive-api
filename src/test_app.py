import pytest
from .app import *

def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))

@pytest.fixture
def client(request):
    test_client = app.test_client()

    def teardown():
        pass # databases and resourses have to be freed at the end. But so far we don't have anything

    request.addfinalizer(teardown)
    return test_client

def test_root(client):
    response = client.get('/')
    assert b'Game Hive Player API' in response.data
    assert response.status_code == 200

def test_create_player_bad_request(client):
    response = post_json(client, '/player/create/', {})
    assert response.status_code == 400

def test_create_player_success(client):
    pass

def test_update_player_bad_request(client):
    response = post_json(client, '/player/update/', {})
    assert response.status_code == 400

def test_update_player_success(client):
    pass

def test_delete_player_bad_request(client):
    response = post_json(client, '/player/delete/', {})
    assert response.status_code == 400

def test_get_guild_skill_points(client):
    pass

def test_create_guild_bad_request(client):
    response = post_json(client, '/guild/create/', {})
    assert response.status_code == 400

def test_create_guild_success(client):
    pass

def test_update_guild_bad_request(client):
    response = post_json(client, '/guild/update/', {})
    assert response.status_code == 400

def test_update_guild_success(client):
    pass

def test_delete_guild_bad_request(client):
    response = post_json(client, '/guild/update/', {})
    assert response.status_code == 400

def test_delete_guild_success(client):
    pass

def test_create_item_bad_request(client):
    response = post_json(client, '/item/create/', {})
    assert response.status_code == 400

def test_create_item_success(client):
    pass

def test_update_item_bad_request(client):
    response = post_json(client, '/item/update/', {})
    assert response.status_code == 400

def test_update_item_success(client):
    pass

def test_delete_item_bad_request(client):
    response = post_json(client, '/item/update/', {})
    assert response.status_code == 400

def test_delete_item_success(client):
    pass

def test_random_request(client):
    response = post_json(client, '/random-url/', {})
    assert response.status_code == 404
