import base64
import logging
import os
import urllib
from dataclasses import dataclass

import dotenv

from .checker import SlotChecker
from .config import stores_from_config
from .config import twilio_config
from .config import users_from_config
from .models import UserStoreStatus
from .notifier import UserNotifier
from .status import StatusStore
from .users import UserStore


dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("instachecker")


def get_store(stores, store_id):
    for store in stores:
        if store.id == store_id:
            return store


def check_stores(_event=None, _ctx=None):
    checker = SlotChecker(os.environ["REMEMBER_USER_TOKEN"])
    stores = stores_from_config()

    users = users_from_config()
    twilio_conf = twilio_config()
    notifier = UserNotifier(twilio_conf)

    status_store = StatusStore(f"StatusesTable")

    for user in users:
        changes = []
        for store_id in user.store_ids:
            store = get_store(stores, store_id)
            last_status = status_store.get_status(user.id, store.id)
            current_status = checker.get_status(user, store)
            if last_status != current_status:
                changes.append(UserStoreStatus(user.id, store.id, current_status))

        for change in changes:
            store = get_store(stores, change.store_id)
            if change.status == "AVAILABLE" and user.messaging_enabled:
                notifier.notify(user, store)
            status_store.set_status(user.id, store.id, change.status)


def seed_users(_event, _ctx):
    users = users_from_config()
    user_store = UserStore("UsersTable")

    for user in users:
        try:
            user = user_store.create(user.dict())
        except Exception as e:  # pylint: disable=broad-except
            log.error(str(e))


def sms(event, _ctx):
    body = base64.b64decode(event["body"]).decode("utf-8")
    message = dict(urllib.parse.parse_qsl(body))
    print("MESSAGE\n", message)
    from_number = message["From"]
    body = message["Body"]
    print(body)

    user_store = UserStore("UsersTable")

    user = user_store.get(from_number)

    if not user:
        resp = "idkwtfya"
    elif body.lower().strip() in ["stop", "pause", "hold", "shut up", "fuck off"]:
        if not user.messaging_enabled:
            resp = "I got it the first time. I'll continue fucking off."
        else:
            resp = "Roger that. Standing by. Send 'ready and willing' to continue messaging."
        user_store.disable_messaging(user.id)
    elif body.lower().strip() in ["continue", "start", "ready and willing"]:
        resp = "I'm on it! Send a friendly 'fuck off' to pause messaging."
        user_store.enable_messaging(user.id)
    else:
        resp = "I don't understand. Try using English."

    return {
        "statusCode": 200,
        "body": str(resp),
    }


if __name__ == "__main__":
    check_stores()
