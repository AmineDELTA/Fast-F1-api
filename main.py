from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from database import create_table
from models import Driver, Team
from sqlalchemy.orm import Session
from database import SessionLocal
import requests
from schemas import DriverCreate, DriverOut, TeamCreate, TeamOut, TeamUpdate, DriverRankingOut, TeamRankingOut
from crud import (get_team, get_driver, get_circuit, get_driver_ranks, get_team_ranks, get_driver_rank, get_team_rank, update_team, create_team, create_driver)
from rate_limit import rate_limiter

app = FastAPI()
create_table()

app.middleware("http")(rate_limiter)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDependency = Annotated[Session, Depends(get_db)] #this is pretty nice


@app.get("/") #idk if i should delete this thing
def read_root():
    return {"message": "Welcome"}


@app.get("/drivers/{number}")
def get_driver_route(number: int, db: SessionDependency):
    driver = get_driver(db, number)
    if not driver:  # 
        raise HTTPException(status_code=404, detail="driver not found")
    endpoints = {   #these endpoints are not working well, and idk why
        # "laps": f"https://api.openf1.org/v1/laps?driver_number={number}&session_key=latest",
        # "pit": f"https://api.openf1.org/v1/pit?driver_number={number}&session_key=latest",
        # "position": f"https://api.openf1.org/v1/position?driver_number={number}&meeting_key=latest",
        # "stint": f"https://api.openf1.org/v1/stints?driver_number={number}&session_key=latest",
        # "radio": f"https://api.openf1.org/v1/team_radio?driver_number={number}&session_key=latest",
    }
    results = {}
    for key, url in endpoints.items():
        response = requests.get(url)
        if response.status_code == 200:
            results[key] = response.json()
        else:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to fetch {key} data from OpenF1 (status code: {response.status_code})",
            )
    return {
        "driver_info": {
            "name": f"{driver.first_name} {driver.last_name}",
            "number": driver.number,
            "nationality": driver.nationality,
            "age": driver.age,
            "team":{
                "id":driver.team_name_id,
                "name":team.name if (team := get_team(db, driver.team_name_id)) else None, # := is kinda nice ngl
            }
        },
        "live_info": results, #this does not return anything for now
    }


@app.post("/drivers/create", response_model=DriverOut)
def create_driver_route(driver: DriverCreate, db: SessionDependency):
    existing = db.query(Driver).filter((Driver.number == driver.number)|(Driver.first_name.ilike(driver.first_name))).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Driver number {driver.number} already exists. Use a unique number.",
        )
    team_id = None
    if driver.team_name:
        team = db.query(Team).filter(Team.name.ilike(driver.team_name)).first()
        if not team:
            raise HTTPException(status_code=404, detail=f"Team '{driver.team_name}' not found")
        team_id = team.id  # CHANGE: teamm.id → team.id

    db_driver = Driver(
        first_name=driver.first_name,
        last_name=driver.last_name,
        number=driver.number,
        age=driver.age,
        nationality=driver.nationality,
        team_name_id=team_id,
    )
    return create_driver(db, db_driver)


@app.get("/drivers")
def get_all_drivers_route(db: SessionDependency):
    all_drivers = db.query(Driver).all()  # CHANGE: les_drivers → all_drivers
    return[{
        "number": d.number,
        "name": f"{d.first_name} {d.last_name}",
        "team_id": d.team_name_id
    } for d in all_drivers]  # CHANGE: les_drivers → all_drivers


@app.get("/teams/{id}")
def get_team_route(id: int, db: SessionDependency):
    team = get_team(db, id)
    if not team:
        raise HTTPException(status_code=404, detail="team not found")

    driver_list = []
    for driver in team.drivers:
        driver_list.append(
            {
                "first_name": driver.first_name,
                "last_name": driver.last_name,
                "number": driver.number,
                "age": driver.age,
                "nationality": driver.nationality,
            }
        )
    return{
        "name": team.name,
        "victories": team.victories,
        "championships": team.championships,
        "drivers": driver_list,
    }


@app.get("/rankings/teams/{name}", response_model=TeamRankingOut)
def get_team_ranking(name: str, db: SessionDependency):
    rank = get_team_rank(db, name)
    if not rank:
        raise HTTPException(status_code=404, detail="Team ranking not found")
    team = db.query(Team).filter(Team.name == name).first()
    drivers = [f"{d.first_name} {d.last_name}" for d in team.drivers] if team else []
    return {
        "team_name": name,
        "drivers": drivers,
        "position": rank.position,
        "points": rank.points,
    }


@app.post("/teams/create", response_model=TeamOut)
def create_team_route(team: TeamCreate, db: SessionDependency):

    existing_team = db.query(Team).filter(Team.name == team.name).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="Team already exists")

    db_team = Team(
        name=team.name, victories=team.victories, championships=team.championships
    )
    return create_team(db, db_team)


@app.get("/circuits/{id}")
def get_circuit_route(id: int, db: SessionDependency):
    circuit = get_circuit(db, id)
    if not circuit:
        raise HTTPException(status_code=404, detail="circuit not found")
    return{
        "name": circuit.name,
        "location": circuit.location,
        "length_km": circuit.length,
        "laps": circuit.laps,
        "lap_record": circuit.lap_record,
        "race_distance_km": circuit.race_distance,
        "corners": circuit.num_corners,
    }


@app.get("/rankings/drivers")
def get_drivers_ranks_route(db: SessionDependency):
    driver_ranks = get_driver_ranks(db)
    if not driver_ranks:
        raise HTTPException(status_code=404, detail="driver ranks not found")

    result = []
    for rank in driver_ranks:
        driver = db.query(Driver).filter(Driver.id == rank.driver_id).first()
        if not driver:
            continue
        result.append(
            {
                "driver_name": f"{driver.first_name} {driver.last_name}",
                "driver_number": driver.number,
                "team_id": driver.team_name_id,
                "position": rank.position,
                "points": rank.points,
            }
        )
    return result


@app.get("/rankings/drivers/{number}", response_model=DriverRankingOut)
def get_driver_ranking_route(number: int, db: SessionDependency):
    rank = get_driver_rank(db, number)
    if not rank:
        raise HTTPException(status_code=404, detail="Driver ranking not found")
    driver = get_driver(db, number)
    team = get_team(db, driver.team_name_id) if driver.team_name_id else None
    return{
        "driver_number": number,
        "driver_name": f"{driver.first_name} {driver.last_name}",
        "team": team.name if team else None,
        "position": rank.position,
        "points": rank.points
    }

@app.get("/rankings/teams")
def get_teams_ranks_route(db: SessionDependency):
    team_ranks = get_team_ranks(db)
    if not team_ranks:
        raise HTTPException(status_code=404, detail="team ranks not found")

    result = []
    for rank in team_ranks:
        team = db.query(Team).filter(Team.id == rank.team_id).first()
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


@app.patch("/teams/{team_id}")
def update_team_route(team_id: int, updates: TeamUpdate, db: SessionDependency):
    team = update_team(db, team_id, updates)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.get("/live") # useless for now :(
def get_live():
    endpoints = {"race_control": "https://api.openf1.org/v1/race_control?session_key=latest",
        "sessions": "https://api.openf1.org/v1/sessions?session_key=latest",
        "weather": "https://api.openf1.org/v1/weather?meeting_key=latest",
    }
    results = {}
    for key, url in endpoints.items():
        response = requests.get(url)
        if response.status_code == 200:
            results[key] = response.json()
        else:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to fetch {key} data from OpenF1 (status code: {response.status_code})",
            )

    return results
