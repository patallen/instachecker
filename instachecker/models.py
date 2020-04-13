from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class User:
    name: str
    phone_number: str
    address_id: int
    messaging_enabled: bool
    store_ids: List[int]

    @property
    def id(self):
        return self.phone_number

    def dict(self):
        return dict(
            name=self.name,
            phone_number=self.phone_number,
            address_id=self.address_id,
            messaging_enabled=self.messaging_enabled,
            store_ids=self.store_ids,
        )


@dataclass
class Store:
    id: int
    name: str


@dataclass
class Slot:
    starts_at: datetime
    ends_at: datetime


@dataclass
class UserStoreStatus:
    user_id: int
    store_id: int
    status: str
