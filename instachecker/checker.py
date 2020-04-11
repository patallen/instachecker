import logging
from typing import List

import requests

from .models import Slot, Store

log = logging.getLogger("delcheck.checker")


class SlotChecker:
    def __init__(self, remember_user_token):
        self.remember_user_token = remember_user_token
        self.session = requests.Session()

    def build_headers(self):
        return {"cookie": f"remember_user_token={self.remember_user_token};"}

    @staticmethod
    def build_url(store_id):
        return f"https://www.instacart.com/v3/retailers/{store_id}/delivery_options"

    def build_request(self, store_id):
        headers = self.build_headers()
        url = self.build_url(store_id)
        return requests.Request("GET", url, headers=headers)

    def check_store(self, store: Store) -> List[Slot]:
        request = self.build_request(store.id)
        prepared = request.prepare()
        res = self.session.send(prepared)
        data = res.json()
        options = data["tracking_params"]["delivery_options"]
        return [Slot(starts_at=o["starts_at"], ends_at=o["ends_at"]) for o in options]
