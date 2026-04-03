import requests

url = "https://api.github.com/repos/boto/boto3/commits"
params = {"per_page": 50}
headers = {"Accept": "application/vnd.github+json"}

response = requests.get(url, params=params, headers=headers)
commits = response.json()

print(f"Fetched {len(commits)} commits\n")

for c in commits:
    sha     = c["sha"][:7]
    author  = c["commit"]["author"]["name"]
    date    = c["commit"]["author"]["date"]
    message = c["commit"]["message"].splitlines()[0]
    print(f"{sha}  {date}  {author:<20}  {message}")
