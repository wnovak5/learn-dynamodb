import boto3

dynamodb = boto3.client('dynamodb')

response = dynamodb.create_table(
    TableName='commits',
    KeySchema=[
        {"AttributeName": "repo", "KeyType": "HASH"},   # partition key
        {"AttributeName": "sha",  "KeyType": "RANGE"},  # sort key
    ],
    AttributeDefinitions=[
        {"AttributeName": "repo", "AttributeType": "S"},
        {"AttributeName": "sha",  "AttributeType": "S"},
    ],
    BillingMode="PAY_PER_REQUEST",
)

print(f"Table status: {response['TableDescription']['TableStatus']}")
print("Table 'commits' is being created.")
