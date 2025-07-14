def test_create_team(client):
    response = client.post("/teams/create", json={"name": "Ferrari", "victories": 243, "championships": 16})
    assert response.status_code == 200
    assert response.json()["name"] == "Ferrari"

def test_get_team_with_drivers(client, test_team):
    response = client.get(f"/teams/{test_team.id}")
    assert response.status_code == 200
    assert len(response.json()["drivers"]) == 1
    assert response.json()["drivers"][0]["number"] == test_team.drivers[0].number

def test_update_team(client, test_team):
    response = client.patch(f"/teams/{test_team.id}", json={"victories": 126})
    assert response.status_code == 200
    assert response.json()["victories"] == 126