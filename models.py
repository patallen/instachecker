from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class User:
    name: str
    phone_number: str
    store_ids: List[int]


@dataclass
class Store:
    id: int
    name: str
    location: str


@dataclass
class Slot:
    starts_at: datetime
    ends_at: datetime
