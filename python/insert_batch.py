"""
4. Insert multiple records using batch_writer.

batch_writer handles:
  - Grouping items into batches of up to 25 (the DynamoDB maximum).
  - Automatic retries for unprocessed items.
"""

import logging
from datetime import datetime, timezone, timedelta

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TABLE_NAME = "SensorReadings"


def insert_batch(table_name=TABLE_NAME):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    now = datetime.now(timezone.utc)

    # Generate sample readings for two devices over the last 5 minutes.
    items = []
    for device in ["sensor-01", "sensor-02"]:
        for i in range(5):
            items.append(
                {
                    "device_id": device,
                    "timestamp": (now - timedelta(minutes=i)).isoformat(),
                    "temperature": 70.0 + i,
                    "humidity": 40.0 + i * 2,
                    "location": "Lab A" if device == "sensor-01" else "Lab B",
                }
            )

    try:
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
        logger.info("Batch-inserted %d items across 2 devices.", len(items))
    except ClientError as e:
        logger.error("Batch write failed: %s", e)
        raise


if __name__ == "__main__":
    insert_batch()
