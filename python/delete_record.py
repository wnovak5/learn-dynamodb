"""
7. Delete a record by its primary key.

With a composite key (partition + sort), you must provide BOTH
values to identify the exact item to delete.

This script finds the oldest reading for a device and deletes it.
"""

import logging

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TABLE_NAME = "SensorReadings"


def delete_record(device_id="sensor-01", table_name=TABLE_NAME):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    # Find the oldest reading for this device.
    try:
        response = table.query(
            KeyConditionExpression=Key("device_id").eq(device_id),
            ScanIndexForward=True,  # ascending (oldest first)
            Limit=1,
        )
    except ClientError as e:
        logger.error("Query failed: %s", e)
        raise

    if not response["Items"]:
        logger.warning("No items found for device '%s'.", device_id)
        return

    item = response["Items"][0]
    logger.info(
        "Deleting: device_id='%s', timestamp='%s'",
        item["device_id"],
        item["timestamp"],
    )

    try:
        table.delete_item(
            Key={
                "device_id": item["device_id"],
                "timestamp": item["timestamp"],
            }
        )
        logger.info("Deleted successfully.")
    except ClientError as e:
        logger.error("Delete failed: %s", e)
        raise


if __name__ == "__main__":
    delete_record()
