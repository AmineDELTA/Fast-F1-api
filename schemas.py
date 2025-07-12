from pydantic import BaseModel, Field
from typing import Optional
from pydantic import field_validator
 
class DriverBase(BaseModel):

    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    number: int = Field(..., ge=1, le=99)
    age: int = Field(..., ge=15)
    nationality: str = Field(...)
    team_name: Optional[str] = None


class DriverCreate(DriverBase):
    @field_validator("nationality")#this field validator thing still confuses me
    def validate_nationality(cls, value: str) -> str:
        if len(value) > 50:
            raise ValueError("Nationality must be ≤ 50 chars")
        return value


class DriverUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    number: Optional[int] = None
    age: Optional[int] = None
    nationality: Optional[str] = None


class DriverOut(DriverBase):
    id: int
    team_id: Optional[int] = Field(None, description = "Linked team ID for API lookups", example=1)
    class Config:
        from_attributes = True


class TeamBase(BaseModel):
    name: str = Field(..., example="Mercedes")
    victories: int = Field(..., example=124)
    championships: int = Field(..., example=8)


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    victories: Optional[int] = Field(None, ge=0)
    championships: Optional[int] = Field(None, ge=0)

class RankingOut(BaseModel):
    position: int
    points: int
    wins: Optional[int] = None

class DriverRankingOut(RankingOut):
    driver_name: str
    driver_number: int
    team: Optional[str]

class TeamRankingOut(RankingOut):
    team_name: str = Field(..., description="Official team name")
    drivers: list[str] = Field(..., description="List of driver full names")
    

class TeamOut(TeamBase):
    id: int

    class Config:
        from_attributes = True
