"""
6. Query items by partition key (and optionally filter on the sort key).

This is the ACCESS-PATTERN approach to DynamoDB:
  - You designed the table with device_id as the partition key
    because your app frequently asks "give me all readings for sensor X."
  - Query is efficient: it only reads items that share the given
    partition key, unlike Scan which reads everything.

The KeyConditionExpression below also demonstrates filtering on the
sort key (timestamp) to get only recent readings.
"""

import logging

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TABLE_NAME = "SensorReadings"


def query_by_key(device_id="sensor-01", table_name=TABLE_NAME):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    # --- Example A: all readings for a device ---
    logger.info("All readings for '%s':", device_id)

    try:
        response = table.query(
            KeyConditionExpression=Key("device_id").eq(device_id),
        )
    except ClientError as e:
        logger.error("Query failed: %s", e)
        raise

    for item in response["Items"]:
        logger.info("  %s  temp=%s", item["timestamp"], item.get("temperature"))

    # --- Example B: readings after a specific timestamp ---
    cutoff = "2024-01-01T00:00:00"
    logger.info("Readings for '%s' after %s:", device_id, cutoff)

    try:
        response = table.query(
            KeyConditionExpression=(
                Key("device_id").eq(device_id) & Key("timestamp").gt(cutoff)
            ),
            ScanIndexForward=False,  # newest first
            Limit=10,
        )
    except ClientError as e:
        logger.error("Query with cutoff failed: %s", e)
        raise

    for item in response["Items"]:
        logger.info("  %s  temp=%s", item["timestamp"], item.get("temperature"))

    return response["Items"]


if __name__ == "__main__":
    query_by_key()
