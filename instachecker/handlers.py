import logging
import os

import dotenv

from .checker import SlotChecker
from .config import stores_from_config
from .config import twilio_config
from .config import users_from_config
from .notifier import UserNotifier
from .status import StatusStore

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("instachecker")


def check_stores(_event=None, _ctx=None):
    checker = SlotChecker(os.environ["REMEMBER_USER_TOKEN"])
    stores = stores_from_config()

    users = users_from_config()
    twilio_conf = twilio_config()
    notifier = UserNotifier(users, twilio_conf)

    status_store = StatusStore(f"StatusTable")

    for store in stores:
        current_status = status_store.get_status(store.id)
        slots = checker.check_store(store)
        if not slots:
            log.info("No slots for %s in %s", store.name, store.location)
            if current_status == "AVAILABLE":
                status_store.set_status(store.id, 'UNAVAILABLE')
            continue

        if current_status == "UNAVAILABLE":
            notifier.notify_users(store, slots)
            status_store.set_status(store.id, "AVAILABLE")


if __name__ == "__main__":
    check_stores()
