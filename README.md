# learn-dynamodb

Learn how to work with DynamoDB


## Key Concepts

**The Core Mental Model** - Think of DynamoDB like a distributed filing cabinet. The partition key determines which drawer your data goes in (which physical server/shard). The sort key determines how items are ordered within that drawer. But understanding how these work together is an important design consideration.

### Partition Keys and Sort Keys

DynamoDB tables require a **primary key** to uniquely identify each item. There are two types:

- **Partition Key (PK)** — A single attribute that DynamoDB uses to distribute data across internal partitions. Every item must have a partition key. DynamoDB hashes this value to determine which physical partition stores the item. Example: `user_id`.

- **Sort Key (SK)** — An optional second attribute that, combined with the partition key, forms a **composite primary key**. Items with the same partition key are stored together and sorted by the sort key. Example: `timestamp`.

**Why this matters:**

| Primary Key Type | Uniqueness | Use Case |
|---|---|---|
| Partition key only | Each PK value must be unique | Simple lookups (one user, one config) |
| Partition key + Sort key | The *combination* must be unique | One-to-many relationships (one user, many orders) |

### Access Patterns vs. Data Entities

In a relational database you model around **entities** (normalize tables, then join at query time). In DynamoDB you model around **access patterns** — the questions your application needs to answer.

**Relational thinking:** "I have Users, Orders, and Products — let me create three tables and join them."

**DynamoDB thinking:** "My app needs to: (1) get a user's profile, (2) list a user's recent orders, (3) look up an order by ID. Let me design keys that serve all three queries in a single table."

This is called **single-table design**. You store different entity types in the same table and use generic key names like `PK` and `SK` with prefixed values:

```
PK              SK                  Data
USER#alice      PROFILE             {name, email, ...}
USER#alice      ORDER#2024-001      {total, status, ...}
USER#alice      ORDER#2024-002      {total, status, ...}
ORDER#2024-001  METADATA            {items, shipping, ...}
```

This lets you fetch a user and all their orders in a **single query** — something that would require a JOIN in SQL.

**Bottom line:** Design your table around *how you will read the data*, not around what the data looks like.


## Creating a Table with the AWS CLI

```bash
aws dynamodb create-table \
  --table-name SensorReadings \
  --attribute-definitions \
    AttributeName=device_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=S \
  --key-schema \
    AttributeName=device_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST
```

- `HASH` = partition key
- `RANGE` = sort key
- `PAY_PER_REQUEST` = on-demand billing (no capacity planning needed for learning)
- You only define attributes that are part of the key schema. DynamoDB is schemaless — other attributes are added at write time.

Check that the table is active:

```bash
aws dynamodb describe-table --table-name SensorReadings --query "Table.TableStatus"
```


## Scanning for the 10 Most Recent Records (CLI)

A **Scan** reads every item in the table, so it is expensive on large tables. For small tables or one-off exploration it is fine:

```bash
aws dynamodb scan \
  --table-name SensorReadings \
  --limit 10 \
  --scan-filter '{
    "timestamp": {
      "AttributeValueList": [{"S": "2024-01-01T00:00:00Z"}],
      "ComparisonOperator": "GE"
    }
  }'
```

To get truly "most recent" records efficiently, you should **Query** a known partition key and sort descending:

```bash
aws dynamodb query \
  --table-name SensorReadings \
  --key-condition-expression "device_id = :did" \
  --expression-attribute-values '{":did": {"S": "sensor-01"}}' \
  --scan-index-forward false \
  --limit 10
```

`--scan-index-forward false` sorts the sort key in descending order (newest first).


## Python Scripts

The `python/` directory contains scripts that cover all CRUD basics:

| # | Script | Operation | What it demonstrates |
|---|--------|-----------|----------------------|
| 1 | `create_table.py` | Create | Build a table with a composite key |
| 2 | `insert_record.py` | Create | Put a single item |
| 3 | `read_record.py` | Read | Get a single item by its full primary key |
| 4 | `insert_batch.py` | Create | Write multiple items in one call |
| 5 | `scan_all.py` | Read | Scan an entire table (paginated) |
| 6 | `query_by_key.py` | Read | Query items by partition key (access-pattern-driven) |
| 7 | `delete_record.py` | Delete | Remove an item by its primary key |

### Setup

```bash
pip install boto3
```

Make sure your AWS credentials are configured (`aws configure` or environment variables).

### Run order

```bash
cd python/
python create_table.py
python insert_record.py
python insert_batch.py
python scan_all.py
python read_record.py
python query_by_key.py
python delete_record.py
```
