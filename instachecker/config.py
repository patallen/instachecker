import os

import yaml

from .models import Store, User


def stores_from_config():
    with open("./confs/store-config.yml") as f:
        stores = yaml.safe_load(f.read())
        return [Store(**store) for store in stores]


def users_from_config():
    with open("./confs/users-config.yml") as f:
        users = yaml.safe_load(f.read())
        return [User(**user) for user in users]


def twilio_config():
    return {
        "account_sid": os.environ["TWILIO_ACCOUNT_SID"],
        "auth_token": os.environ["TWILIO_AUTH_TOKEN"],
        "from_number": os.environ["TWILIO_FROM_NUMBER"],
    }
