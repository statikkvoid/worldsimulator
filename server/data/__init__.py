from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PersonStats(BaseModel):
    strength: int
    perception: int
    endurance: int
    charisma: int
    intelligence: int
    agility: int
    luck: int


class PersonHealth(BaseModel):
    injury: str
    time_left: int


class Person(BaseModel):
    id: str
    firstname: str
    lastname: str
    address: str
    email: str
    born: datetime
    is_alive: bool = True

    health_issues: Optional[PersonHealth] = None

    affected_by: List[str] = []

    stats: PersonStats


class Relation(BaseModel):
    id: str
    person1: str
    person2: str
    start_date: datetime

    is_active: bool

    children: List[Person]


class Event(BaseModel):
    id: str
    event: dict
    days_left: Optional[int]
