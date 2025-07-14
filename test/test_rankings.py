def test_driver_ranking(client, test_driver):
    client.post(
        "/rankings/drivers",
        json={
            "driver_id": test_driver.id,
            "position": 1,
            "points": 256
        }
    )
    
    response = client.get(f"/rankings/drivers/{test_driver.number}")
    assert response.status_code == 200
    assert response.json()["position"] == 1