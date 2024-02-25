from main import rate_limit



def test_read_root(client):
    response = client.get("")

    assert response.status_code == 200, response.txt
    data = response.json()
    assert data["message"] == "Hello World"


def test_read_root_rate_limit(client):

    for _ in range(100):
        response = client.get("")

    assert response.status_code == 429, response.text
    data = response.json()
    assert data['detail'] == "Too Many Requests"