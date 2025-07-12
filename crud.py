from sqlalchemy.orm import Session
from models import Driver, Team, Circuit, TeamRank, DriverRank

#idk if i'm gonna use all of them
def get_driver(db: Session, number: int):
    return db.query(Driver).filter(Driver.number == number).first()


def create_driver(db: Session, driver: Driver):
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver


def get_driver_rank(db: Session, number: int):
    driver_UNI = db.query(Driver).filter(Driver.number == number).first()
    if not driver_UNI:
        return None
    return db.query(DriverRank).filter(DriverRank.driver_id == driver_UNI.id).first()


def get_driver_ranks(db: Session):
    return db.query(DriverRank).order_by(DriverRank.position.asc()).all()


def get_all_drivers(db: Session):
    return db.query(Driver).all()


def update_driver(db: Session, number: int, updates: dict):
    driver = db.query(Driver).filter(Driver.number == number).first()
    if driver:
        for key, value in updates.items():
            setattr(driver, key, value)
        db.commit()
        db.refresh(driver)
    return driver


def delete_driver(db: Session, number: int):
    driver = db.query(Driver).filter(Driver.number == number).first()
    if driver:
        db.delete(driver)
        db.commit()
    return driver
    
    
def get_team(db: Session, id: int):
    return db.query(Team).filter(Team.id == id).first()


def create_team(db: Session, Team: Team):
    db.add(Team)
    db.commit()
    db.refresh(Team)
    return Team


def get_team_rank(db: Session, name: str):
    team = db.query(Team).filter(Team.name == name).first()
    if not team:
        return None
    return db.query(TeamRank).filter(TeamRank.team_id == team.id).first()


def get_team_ranks(db: Session):
    return db.query(TeamRank).order_by(TeamRank.position.asc()).all()


def get_circuit(db: Session, id: int):
    return db.query(Circuit).filter(Circuit.id == id).first()


def create_circuit(db: Session, circuit: Circuit):
    db.add(circuit)
    db.commit()
    db.refresh(circuit)
    return circuit


def delete_team(db: Session, team_id: int):
    team = db.query(Team).filter(Team.id == team_id).first()
    if team:
        db.delete(team)
        db.commit()
    return team
    

def update_team(db: Session, team_id: int, updates: dict):
    team = db.query(Team).filter(Team.id == team_id).first()
    if team:
        for key, value in updates.items():
            setattr(team, key, value)
        db.commit()
        db.refresh(team)
    return team