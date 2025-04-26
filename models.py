from sqlalchemy import Column, Integer, String, ForeignKey, Float
from .database import Base


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    team_name_id = Column(Integer, ForeignKey("teams.id"))
    name = Column(String, unique=True)
    number = Column(Integer, unique=True)
    age = Column(Integer)
    nationality = Column(String)


class Teams(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    team_principal = Column(String)
    car_model = Column(String)
    base = Column(String)
    drivers = Column(Integer)
    victories = Column(Integer)
    podiums = Column(Integer)


class Circuit(Base):
    __tablename__ = "circuits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    length = Column(Float)
    laps = Column(Integer)
    lap_record = Column(String)
    race_distance = Column(Float)
    num_corners = Column(Integer)


class DriverRank(Base):
    __tablename__ = "driver_rank"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    points = Column(Integer)
    position = Column(Integer)


class TeamRank(Base):
    __tablename__ = "team_rank"

    id = Column(Integer, primary_key=True, index=True)
    team_name_id = Column(Integer, ForeignKey("teams.id"))
    points = Column(Integer)
    position = Column(Integer)
