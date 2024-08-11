from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, HttpUrl, Field


class Organizer(BaseModel):
    id: Annotated[int, Field(strict=True, ge=0)]
    name: str


class Duration(BaseModel):
    days: Annotated[int, Field(strict=True, ge=0)]
    hours: Annotated[int, Field(strict=True, ge=0)]


class CTFTimeEvent(BaseModel):
    organizers: list[Organizer]
    ctftime_url: HttpUrl
    ctf_id: Annotated[int, Field(strict=True, ge=1)]
    weight: Annotated[float, Field(strict=True, ge=0)]
    duration: Duration
    live_feed: Optional[str]
    logo: HttpUrl
    id: Annotated[int, Field(strict=True, ge=0)]
    title: str
    start: datetime
    participants: Annotated[int, Field(strict=True, ge=0)]
    location: Optional[str]
    finish: datetime
    description: Optional[str]
    format: str
    is_votable_now: bool
    prizes: Optional[str]
    format_id: Annotated[int, Field(strict=True, ge=0)]
    onsite: bool
    restrictions: Optional[str]
    url: HttpUrl
    public_votable: bool


class CTFTimeResponse(BaseModel):
    events: list[CTFTimeEvent]

    def __str__(self) -> str:
        return f"{self.events=}"
