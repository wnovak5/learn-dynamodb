"""
2. Insert a single record into the SensorReadings table.

Uses the higher-level boto3 *resource* API so you can pass
native Python types instead of DynamoDB's {"S": "..."} format.
"""

import logging
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TABLE_NAME = "SensorReadings"


def insert_record(table_name=TABLE_NAME):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    item = {
        "device_id": "sensor-01",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": 72.5,
        "humidity": 45.2,
        "location": "Lab A",
    }

    try:
        table.put_item(Item=item)
        logger.info(
            "Inserted item: device_id=%s, timestamp=%s",
            item["device_id"],
            item["timestamp"],
        )
    except ClientError as e:
        logger.error("Failed to insert item: %s", e)
        raise


if __name__ == "__main__":
    insert_record()
