import boto3


class StatusStore:
    def __init__(self, table_name):
        self.dynamo = boto3.resource("dynamodb")
        # pylint: disable=no-member
        self.table = self.dynamo.Table(table_name)

    def get_status(self, user_id, store_id):
        try:
            response = self.table.get_item(
                Key={"user_id": user_id, "store_id": store_id}
            )
            return response["Item"]["store_status"]
        except KeyError:
            self.table.put_item(
                Item={
                    "user_id": user_id,
                    "store_id": store_id,
                    "status_": "UNAVAILABLE",
                }
            )
            return "UNAVAILABLE"

    def set_status(self, user_id, store_id, status):
        self.table.update_item(
            Key={"user_id": user_id, "store_id": store_id},
            UpdateExpression="set status_ = :s",
            ExpressionAttributeValues={":s": status},
        )
