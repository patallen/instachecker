import logging
import random

from twilio.rest import Client


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("instachecker.notifier")


def random_name():
    names = [
        "The Insta-cartographer",
        "Carty B. Checkin' Out",
        "Instagrabber ;)",
        "Bim Bam Margera",
    ]
    return names[random.randint(0, len(names) - 1)]


class UserNotifier:
    def __init__(self, users, twilio_config):
        self.users = users
        self.twilio_config = twilio_config
        self.twilio = Client(twilio_config["account_sid"], twilio_config["auth_token"])

    @staticmethod
    def build_message_body(user, store, slots):
        is_or_are = "is" if len(slots) == 1 else "are"
        with_s = "s" if len(slots) > 1 else ""
        slot_count = len(slots)

        body = f"""Hi, {user.name}!

There {is_or_are} {slot_count} delivery slot{with_s} available at {store.name} in {store.location}.

www.instacart.com

Yours truly,
{random_name()}
"""
        return body

    def notify_users(self, store, slots):
        users = [u for u in self.users if store.id in u.store_ids]
        log.info(
            "Notifying %d users of available slots at %s in %s",
            len(users),
            store.name,
            store.location,
        )

        from_number = self.twilio_config["from_number"]
        for user in users:
            body = self.build_message_body(user, store, slots)
            self.twilio.messages.create(
                to=user.phone_number, from_=from_number, body=body
            )
