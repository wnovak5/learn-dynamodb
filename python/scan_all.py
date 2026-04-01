"""
5. Read ALL records from the table using Scan (with pagination).

Important: Scan reads every item in the table. It is fine for small
tables or one-off exploration, but expensive on large tables.

DynamoDB returns at most 1 MB per Scan call. If there is more data,
the response includes a LastEvaluatedKey that you pass as
ExclusiveStartKey in the next call.
"""

import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TABLE_NAME = "SensorReadings"


def scan_all(table_name=TABLE_NAME):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    all_items = []

    try:
        response = table.scan()
        all_items.extend(response["Items"])

        # Handle pagination.
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            all_items.extend(response["Items"])
    except ClientError as e:
        logger.error("Scan failed: %s", e)
        raise

    logger.info("Total items in table: %d", len(all_items))

    for item in all_items:
        logger.info(
            "  %s  %s  temp=%s  humidity=%s",
            item["device_id"],
            item["timestamp"],
            item.get("temperature"),
            item.get("humidity"),
        )

    return all_items


if __name__ == "__main__":
    scan_all()
