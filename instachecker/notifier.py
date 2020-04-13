import logging
import random

from twilio.rest import Client


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("instachecker.notifier")


def random_name():
    names = [
        "Don Jr.",
        "Snoop Dogg",
        "Instagrabber ;)",
        "Crazy Pete",
        "Dr. Wally Winkers",
        "J. C. Penny",
    ]
    return names[random.randint(0, len(names) - 1)]


class UserNotifier:
    def __init__(self, twilio_config):
        self.twilio_config = twilio_config
        self.twilio = Client(twilio_config["account_sid"], twilio_config["auth_token"])

    @staticmethod
    def build_message_body(user, store):
        body = f"""Hi, {user.name}!

There are Instacart delivery slots open at {store.name} near you.

Feel free to tell me to "fuck off" if you wish to not be bothered.

Yours truly,
{random_name()}
"""
        return body

    def notify(self, user, store):
        log.info(
            "Notifying user %s (%d) of availabilities at %s near address %d",
            user.name,
            user.id,
            store.name,
            user.address_id,
        )

        from_number = self.twilio_config["from_number"]
        body = self.build_message_body(user, store)
        self.twilio.messages.create(to=user.phone_number, from_=from_number, body=body)
