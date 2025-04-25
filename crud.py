from sqlalchemy.orm import Session
from models import Driver, Teams, Circuit


def get_driver_by_number(db: Session, number: int):
    return db.query(Driver).filter(Driver.number == number).first()

def create_driver(db: Session, driver: Driver):
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver


def get_team_by_name(db: Session, name: str):
    return db.query(Teams).filter(Teams.name == name).first()

def create_team(db: Session, team: Teams):
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def get_circuit_by_name(db.Session, name:str)
    
