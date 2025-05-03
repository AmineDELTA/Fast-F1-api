from typing import Annotated
from fastapi import FastAPI, Depends
from database import create_table
from models import Driver, TeamRank, Teams, DriverRank, Circuit
from sqlalchemy.orm import Session
from database import SessionLocal
import requests


app = FastAPI()
create_table()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDependency = Annotated[Session, Depends(get_db)]


@app.get("/Driver/{driver_number}")
def get_driver_live(driver_number: int, db: SessionDependency):
    driver = db.query(Driver).filter(Driver.number == driver_number).first()
    if not driver:
        return {"error": "Driver not found in database"}
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

    return {
        "driver_info": {
            "name": driver.name,
            "number": driver.number,
            "nationality": driver.nationality,
            "age": driver.age,
            "team_id": driver.team_name_id,  # should we add also the team table ? or link it maybe
        },
        "live_info": results,
    }


@app.get("/Teams/{Team_name}")
def get_teams(Team_id: int, db: SessionDependency):
    Team = db.query(Teams).filter(Teams.id == Team_id).first()
    if not Team:
        return {"error": "Team not found in database"}

    driver_list = []
    for driver in Team.drivers:
        driver_list.append(
            {
                "name": driver.name,
                "number": driver.number,
                "age": driver.age,
                "nationality": driver.nationality,
            }
        )
    return {
        "name": Team.name,
        "victories": Team.victories,
        "championships": Team.championships,
        "drivers": Team.Drivers,
    }


@app.get("/Circuit/{Circuit_name}")
def get_circuit(Circuit_id: int, db: SessionDependency):
    circuit = db.query(Circuit).filter(Circuit.id == Circuit_id).first()
    if not circuit:
        return {"error": "circuit not found in database"}
    return {
        "name": circuit.name,
        "location": circuit.location,
        "length_km": circuit.length,
        "laps": circuit.laps,
        "lap_record": circuit.lap_record,
        "race_distance_km": circuit.race_distance,
        "corners": circuit.num_corners,
    }


@app.get("/Ranking/Drivers")
def get_ranking_driver(db: SessionDependency):
    driver_ranks = db.query(DriverRank).order_by(DriverRank.position.asc()).all()
    if not driver_ranks:
        return {"error": "No driver ranking data found"}

    result = []
    for rank in driver_ranks:
        driver = db.query(Driver).filter(Driver.id == rank.driver_id).first()
        if not driver:
            continue
        result.append(
            {
                "driver_name": driver.name,
                "driver_number": driver.number,
                "team_id": driver.team_name_id,
                "position": rank.position,
                "points": rank.points,
            }
        )
    return result


@app.get("/Ranking/Teams")
def get_ranking_team(db: SessionDependency):
    team_ranks = db.query(TeamRank).order_by(TeamRank.position.asc()).all()
    if not team_ranks:
        return {"error": "No team ranking data found"}

    result = []
    for rank in team_ranks:
        team = db.query(Teams).filter(Teams.id == rank.team_name_id).first()
        if not team:
            continue
        result.append(
            {
                "team_name": team.name,
                "position": rank.position,
                "points": rank.points,
            }
        )
    return result


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
