from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl


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
    live_feed: str | None
    logo: (
        str | None
    )  # TODO @kill_your_soul: Make this a Optional URL (idk why ctftime sometimes doesn't return a logo url)
    id: Annotated[int, Field(strict=True, ge=0)]
    title: str
    start: datetime
    participants: Annotated[int, Field(strict=True, ge=0)]
    location: str | None
    finish: datetime
    description: str | None
    format: str
    is_votable_now: bool
    prizes: str | None
    format_id: Annotated[int, Field(strict=True, ge=0)]
    onsite: bool
    restrictions: str | None
    url: HttpUrl
    public_votable: bool


class CTFTimeResponse(BaseModel):
    events: list[CTFTimeEvent]

    def __str__(self) -> str:
        return f"{self.events=}"
