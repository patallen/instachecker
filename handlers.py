import logging
import os

import dotenv

from checker import SlotChecker
from notifier import UserNotifier
from config import users_from_config
from config import stores_from_config
from config import twilio_config

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("delcheck")


def check_stores(_event=None, _ctx=None):
    checker = SlotChecker(os.environ["REMEMBER_USER_TOKEN"])
    stores = stores_from_config()

    users = users_from_config()
    twilio_conf = twilio_config()
    notifier = UserNotifier(users, twilio_conf)

    for store in stores:
        slots = checker.check_store(store)
        if not slots:
            log.info("No slots for %s in %s", store.name, store.location)
            continue

        notifier.notify_users(store, slots)


if __name__ == "__main__":
    check_stores()
