from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/Driver/{driver_number}")
def get_driver_live(driver_number: int):
    endpoints = {
        "laps": f"https://api.openf1.org/v1/laps?driver_number={driver_number}&session_key=latest",
        "pit": f"https://api.openf1.org/v1/pit?driver_number={driver_number}&session_key=latest",
        "position": f"https://api.openf1.org/v1/position?driver_number={driver_number}&meeting_key=latest",
        "stint": f"https://api.openf1.org/v1/stints?driver_number={driver_number}&session_key=latest",
        "radio": f"https://api.openf1.org/v1/team_radio?driver_number={driver_number}&session_key=latest",
    }
    results = {}
    for key, url in endpoints.items():
        response = requests.get(url)
        if response.status_code == 200:
            results[key] = response.json()
        else:
            results[key] = {"error": f"Failed to fetch {key} data"}

    return results


@app.get("/Teams/{Team_name}")
def get_teams(Team_name: str):
    endpoints = {}


@app.get("/Circuit/{Circuit_name}")
def get_circuit(Circuit_name: str):
    endpoints = {}


@app.get("/Ranking/Driver/{}")
def get_ranking_live():
    endpoints = {}
    results = {}
    for key, url in endpoints.items():
        response = requests.get(url)
        if response.status_code == 200:
            results[key] = response.json()
        else:
            results[key] = {"error": f"Failed to fetch {key} data"}

    return results


@app.get("/Live")
def get_main():
    endpoints = {
        "race_control": "https://api.openf1.org/v1/race_control?session_key=latest",
        "sessions": "https://api.openf1.org/v1/sessions?session_key=latest",
        "weather": "https://api.openf1.org/v1/weather?meeting_key=latest",
    }
    results = {}
    for key, url in endpoints.items():
        response = requests.get(url)
        if response.status_code == 200:
            results[key] = response.json()
        else:
            results[key] = {"error": f"Failed to fetch {key} data"}

    return results
