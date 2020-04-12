import boto3
from botocore.exceptions import ClientError


class StatusStore:
    def __init__(self, table_name):
        self.dynamo = boto3.resource("dynamodb")
        self.table = self.dynamo.Table(table_name)

    def get_status(self, store_id):
        try:
            response = self.table.get_item(Key={"storeId": store_id})
            return response["Item"]["store_status"]
        except KeyError:
            self.table.put_item(
                Item={
                    "storeId": store_id,
                    "store_status": "UNAVAILABLE",
                }
            )
            return "UNAVAILABLE"

    def set_status(self, store_id, status):
        self.table.update_item(
            Key={"storeId": store_id},
            UpdateExpression="set store_status = :s",
            ExpressionAttributeValues={":s": status},
        )
