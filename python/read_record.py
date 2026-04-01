"""
3. Read a single record by its full primary key (partition key + sort key).

You must supply BOTH parts of a composite key to use GetItem.
If you only know the partition key, use Query instead (see query_by_key.py).
"""

import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TABLE_NAME = "SensorReadings"


def read_record(table_name=TABLE_NAME):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    # First, grab one item so we have a valid key to look up.
    try:
        scan = table.scan(Limit=1)
    except ClientError as e:
        logger.error("Failed to scan table: %s", e)
        raise

    if not scan["Items"]:
        logger.warning("Table is empty. Insert a record first.")
        return None

    sample = scan["Items"][0]
    device_id = sample["device_id"]
    timestamp = sample["timestamp"]

    logger.info("Looking up device_id='%s', timestamp='%s' ...", device_id, timestamp)

    try:
        response = table.get_item(
            Key={
                "device_id": device_id,
                "timestamp": timestamp,
            }
        )
    except ClientError as e:
        logger.error("Failed to get item: %s", e)
        raise

    item = response.get("Item")
    if item:
        logger.info("Found item:")
        for key, value in item.items():
            logger.info("  %s: %s", key, value)
    else:
        logger.warning("Item not found.")

    return item


if __name__ == "__main__":
    read_record()
