from pydantic import BaseModel, Field
from typing import Optional
from pydantic import field_validator

# ---- Driver Schemas ----
class DriverBase(BaseModel):
    """Matches the Driver model"""

    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    number: int = Field(..., ge=1, le=99)
    age: int = Field(..., ge=15)
    nationality: str = Field(...)
    team_name: Optional[str] = None


class DriverCreate(DriverBase):
    # Validator 1: Check nationality length
    @field_validator("nationality")
    def validate_nationality(cls, value: str) -> str:
        if len(value) > 50:
            raise ValueError("Nationality must be ≤ 50 chars")
        return value

    # Validator 2: Ensure team_name exists (pseudo-code)
    @field_validator("team_name")
    def validate_team_name(cls, value: str | None) -> str | None:
        if value and value.lower() not in ["ferrari", "mercedes"]:  # Replace with DB check
            raise ValueError("Team must be Ferrari or Mercedes")
        return value


class DriverUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    number: Optional[int] = None
    age: Optional[int] = None
    nationality: Optional[str] = None


class DriverOut(DriverBase):
    id: int

    class Config:
        from_attributes = True


# ---- Team Schemas ----
class TeamBase(BaseModel):
    """Shared fields for all Team schemas"""

    name: str = Field(..., max_length=50, example="Mercedes")
    victories: int
    championships: int = Field(0, ge=0)


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    victories: Optional[int] = None
    championships: Optional[int] = None


class TeamOut(TeamBase):
    id: int

    class Config:
        from_attributes = True
