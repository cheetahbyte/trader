import dataclasses
import datetime
import enum


class Website(enum.IntEnum):
    NotFound = -1
    Tagesschau: int = 0


@dataclasses.dataclass
class Stock:
    wkn: str
    value: float
    date: datetime
    site: Website
