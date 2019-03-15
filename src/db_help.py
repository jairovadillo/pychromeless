import boto3
from boto3.dynamodb.conditions import Key, Attr

class DynamoDB:
    def __init__(self, table):
        self.resource = boto3.resource('dynamodb')
        self.table = self.resource.Table(table)

    def put(self, obj):
        return self.table.put_item(Item=obj)

    def get(self, key):
        return self.table.get_item(Key=key)["Item"]
