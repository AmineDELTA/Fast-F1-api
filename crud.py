from sqlalchemy.orm import Session
from models import Driver, Teams, Circuit, TeamRank, DriverRank


def get_driver(db: Session, number: int):
    return db.query(Driver).filter(Driver.number == number).first()


def create_driver(db: Session, driver: Driver):
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver


def get_UNdriver_rank(db: Session, number: int):
    driver_w = db.query(Driver).filter(Driver.number == number).first()
    if not driver_w:
        return None
    return db.query(DriverRank).filter(DriverRank.driver_id == driver_w.id).first()


def get_driver_ranks(db: Session):
    return db.query(DriverRank).order_by(DriverRank.position.asc()).all()


def get_team(db: Session, id: int):
    return db.query(Teams).filter(Teams.id == id).first()


def create_team(db: Session, team: Teams):
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def get_UNteam_rank(db: Session, name: str):
    team = db.query(Teams).filter(Teams.name == name).first()
    if not team:
        return None
    return db.query(TeamRank).filter(TeamRank.team_name_id == team.id).first()


def get_team_ranks(db: Session):
    return db.query(TeamRank).order_by(TeamRank.position.asc()).all()


def get_circuit(db: Session, id: int):
    return db.query(Circuit).filter(Circuit.id == id).first()


def create_circuit(db: Session, circuit: Circuit):
    db.add(circuit)
    db.commit()
    db.refresh(circuit)
    return circuit
