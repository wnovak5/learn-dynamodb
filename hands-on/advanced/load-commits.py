import httpx
import boto3

REPO = "boto/boto3"

# Fetch commits from GitHub
url = f"https://api.github.com/repos/{REPO}/commits"
params = {"per_page": 50}
headers = {"Accept": "application/vnd.github+json"}

response = httpx.get(url, params=params, headers=headers)
commits = response.json()

# Load directly into DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('commits')

for c in commits:
    item = {
        "repo":         REPO,
        "sha":          c["sha"],
        "author_name":  c["commit"]["author"]["name"],
        "author_email": c["commit"]["author"]["email"],
        "committed_at": c["commit"]["author"]["date"],
        "message":      c["commit"]["message"].splitlines()[0],
        "url":          c["html_url"],
    }
    table.put_item(Item=item)
    print(f"Loaded: {c['sha'][:7]}  {item['committed_at']}  {item['author_name']}")

print(f"\nDone. {len(commits)} commits loaded into 'commits' table.")
