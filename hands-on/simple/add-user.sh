#!/bin/bash

echo "Add a new user to the DynamoDB 'users' table"
echo "---------------------------------------------"

read -p "Username:   " username
read -p "First name: " firstname
read -p "Last name:  " lastname
read -p "Email:      " email
read -p "DOB (YYYY-MM-DD): " dob
read -p "Status (active/inactive/suspended): " status

aws dynamodb put-item \
  --table-name users \
  --item "{
    \"username\":  {\"S\": \"$username\"},
    \"firstname\": {\"S\": \"$firstname\"},
    \"lastname\":  {\"S\": \"$lastname\"},
    \"email\":     {\"S\": \"$email\"},
    \"dob\":       {\"S\": \"$dob\"},
    \"status\":    {\"S\": \"$status\"}
  }"

if [ $? -eq 0 ]; then
  echo "User '$username' added successfully."
else
  echo "Error: failed to insert user." >&2
  exit 1
fi
