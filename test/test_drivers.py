from models import Team

def test_create_driver(client, db_session):
    # First create the required team
    team = Team(name="Red Bull", victories=85, championships=5)
    db_session.add(team)
    db_session.commit()
    
    response = client.post(
        "/drivers/create", 
        json={
            "first_name": "Max",
            "last_name": "Verstappen",
            "number": 1,
            "age": 25,
            "nationality": "Dutch",
            "team_name": "Red Bull"
        }
    )
    assert response.status_code == 200
    assert response.json()["number"] == 1

def test_get_driver(client, test_driver):
    response = client.get(f"/drivers/{test_driver.number}")
    assert response.status_code == 200
    data = response.json()
    assert data["driver_info"]["name"] == "Lewis Hamilton"

    response = client.post("/drivers/create", json={"first_name": "George", "last_name": "Russell", "number": test_driver.number, "age": 24, "nationality": "British"})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]