def test_create_driver(client, test_team):
    response = client.post("/drivers/create", json={
        "first_name": "Max",
        "last_name": "Verstappen",
        "number": 1,
        "age": 25,
        "nationality": "Dutch",
        "team_name": test_team.name
    })
    assert response.status_code == 200
    assert response.json()["number"] == 1

def test_get_driver(client, test_driver):
    response = client.get(f"/drivers/{test_driver.number}")
    assert response.status_code == 200
    data = response.json()
    assert data["driver_info"]["name"] == "Lewis Hamilton"

def test_get_all_drivers(client, test_driver):
    response = client.get("/drivers")
    assert response.status_code == 200
    drivers = response.json()
    assert len(drivers) >= 1
    assert drivers[0]["name"] == "Lewis Hamilton"