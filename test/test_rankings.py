from models import DriverRank

def test_driver_ranking(client, test_driver, db_session):
    driver_rank = DriverRank(
        driver_id=test_driver.id,
        position=1,
        points=256
    )
    db_session.add(driver_rank)
    db_session.commit()
    
    response = client.get(f"/rankings/drivers/{test_driver.number}")
    assert response.status_code == 200
    data = response.json()
    
    assert data["position"] == 1
    assert data["points"] == 256
    assert data["driver_name"] == "Lewis Hamilton"
    assert data["driver_number"] == test_driver.number