import requests

def test_list_players():
    resp = requests.get("http://127.0.0.1:8000/players")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]
    print("test_list_players passed")

def test_get_player():
    resp = requests.get("http://127.0.0.1:8000/players/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert "stats" in data
    print("test_get_player passed")

def test_ai_assistant():
    resp = requests.post("http://127.0.0.1:8000/players/1/ai", json={"question": "How many goals?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    print("test_ai_assistant passed")

if __name__ == "__main__":
    test_list_players()
    test_get_player()
    test_ai_assistant()
