"""
1. Create a DynamoDB table with a composite primary key.

Table: SensorReadings
  Partition key (HASH):  device_id  (String)
  Sort key     (RANGE):  timestamp  (String)

This mirrors the AWS CLI command in the README.
"""

import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TABLE_NAME = "SensorReadings"


def create_table(table_name=TABLE_NAME):
    dynamodb = boto3.client("dynamodb")

    try:
        dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {"AttributeName": "device_id", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "device_id", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        logger.info("Creating table '%s' ...", table_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            logger.warning("Table '%s' already exists.", table_name)
            return
        logger.error("Failed to create table: %s", e)
        raise

    # Wait until the table is active before using it.
    waiter = dynamodb.get_waiter("table_exists")
    waiter.wait(TableName=table_name)
    logger.info("Table '%s' is now ACTIVE.", table_name)


if __name__ == "__main__":
    create_table()
