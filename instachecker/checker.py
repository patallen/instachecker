import logging
from typing import List

import requests

from .models import Slot

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("instachecker.checker")


class SlotChecker:
    def __init__(self, remember_user_token):
        self.remember_user_token = remember_user_token
        self.session = requests.Session()

    def build_headers(self):
        return {"cookie": f"remember_user_token={self.remember_user_token};"}

    @staticmethod
    def build_url(store_id, address_id):
        return f"https://www.instacart.com/v3/retailers/{store_id}/delivery_options?address_id={address_id}"

    def build_request(self, store_id, address_id):
        headers = self.build_headers()
        url = self.build_url(store_id, address_id)
        return requests.Request("GET", url, headers=headers).prepare()

    def get_status(self, user, store) -> List[Slot]:
        request = self.build_request(store.id, user.address_id)
        res = self.session.send(request)
        res.raise_for_status()
        data = res.json()
        slots = data["tracking_params"]["delivery_options"]
        return "AVAILABLE" if slots else "UNAVAILABLE"
