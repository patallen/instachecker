import boto3

from .models import User


class UserStore:
    def __init__(self, table_name):
        self.dynamo = boto3.resource("dynamodb")
        # pylint: disable=no-member
        self.table = self.dynamo.Table(table_name)

    def enable_messaging(self, phone_number):
        self.table.update_item(
            Key={"phone_number": phone_number},
            UpdateExpression="set messaging_enabled = :m",
            ExpressionAttributeValues={":m": True},
        )

    def disable_messaging(self, phone_number):
        self.table.update_item(
            Key={"phone_number": phone_number},
            UpdateExpression="set messaging_enabled = :m",
            ExpressionAttributeValues={":m": False},
        )

    def get(self, phone_number):
        try:
            user_dict = self.table.get_item(Key={"phone_number": phone_number})["Item"]
        except KeyError:
            return None

        return User(**user_dict)

    def create(self, user_dict):
        self.table.put_item(Item=user_dict)
        return User(**user_dict)
