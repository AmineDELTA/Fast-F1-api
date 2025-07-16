def test_create_team(client):
    response = client.post("/teams/create", json={
        "name": "Red Bull",
        "victories": 85,
        "championships": 5
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Red Bull"

def test_get_team(client, test_team):
    response = client.get(f"/teams/{test_team.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_team.name
    assert data["victories"] == 125
    assert data["championships"] == 8

def test_get_team_with_drivers(client, test_team, test_driver):
    response = client.get(f"/teams/{test_team.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["drivers"]) == 1
    assert data["drivers"][0]["number"] == test_driver.number