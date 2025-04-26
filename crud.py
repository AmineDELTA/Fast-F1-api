from sqlalchemy.orm import Session
from models import Driver, Teams, Circuit, TeamRank, DriverRank


def get_driver_by_number(db: Session, number: int):
    return db.query(Driver).filter(Driver.number == number).first()


def create_driver(db: Session, driver: Driver):
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver


def get_driver_rank(db: Session, number: int):
    driver_w = db.query(Driver).filter(Driver.number == number).first()
    if not driver_w:
        return None
    return db.query(DriverRank).filter(DriverRank.driver_id == driver_w.id).first()


def get_team_by_name(db: Session, name: str):
    return db.query(Teams).filter(Teams.name == name).first()


def create_team(db: Session, team: Teams):
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def get_team_rank(db: Session, name: str):
    team = db.query(Teams).filter(Teams.name == name).first()
    if not team:
        return None
    return db.query(TeamRank).filter(TeamRank.team_name_id == team.id).first()


def get_circuit_by_name(db: Session, name: str):
    return db.query(Circuit).filter(Circuit.name == name).first()


def create_circuit(db: Session, circuit: Circuit):
    db.add(circuit)
    db.commit()
    db.refresh(circuit)
    return circuit
