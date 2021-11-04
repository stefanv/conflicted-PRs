import os
import sys
import requests
import string
import argparse
import json


cursor_template = string.Template('after: "$cursor"')

pr_query = string.Template("""
query {
  repository(owner:"$org", name:"$repo") {
    pullRequests(first: 100, states: OPEN, $cursor) {
      edges {
        node {
          number
          url
          mergeable
          createdAt
        }
      },
      pageInfo {
        endCursor
      },
    },
  }
}""")


parser = argparse.ArgumentParser(description='Generate team gallery from GitHub')
parser.add_argument('--org', required=True, help='GitHub organization name')
parser.add_argument('--repo', required=True, help='Repo name in the organization')
args = parser.parse_args()

org = args.org
repo = args.repo


def query(max_queries=100):
    end_cursor = None
    results = []
    for i in range(max_queries):
        if end_cursor:
            cursor = cursor_template.substitute(cursor=end_cursor)
        else:
            cursor = ''

        next_query = pr_query.substitute(cursor=cursor, org=org, repo=repo)
        print(f'Query {i}...', file=sys.stderr)
        request = requests.post(
            'https://api.github.com/graphql',
            json={'query': next_query},
            headers={'Authorization': f'bearer {token}'}
        )
        if request.status_code == 200:
            data = request.json()['data']
            end_cursor = data['repository']['pullRequests']['pageInfo']['endCursor']
            results.extend([e['node'] for e in data['repository']['pullRequests']['edges']])
            if end_cursor is None:
                return results
        else:
            raise RuntimeError("Request received HTTP {request.status_code}: {query}")


token = os.environ.get('GH_TOKEN', None)
if token is None:
    print("No token found.  Please export a GH_TOKEN with permissions "
          "to read team members.", file=sys.stderr)
    sys.exit(-1)


data = query()

with open(f'data/{org}__{repo}.json', 'w') as f:
    json.dump(data, f, indent=2)

m = len(list(p for p in data if p['mergeable'] == 'CONFLICTING'))
n = len(data)

print(f'## {org}/{repo}')
print()
print('### Conflicting ({m}/{n}):')
for pr in data:
    if pr["mergeable"] == "CONFLICTING":
        print(f'- [#{pr["number"]}]({pr["url"]})')

print('### Mergeable ({n - m}/{n}):')
for pr in data:
    if pr["mergeable"] == "MERGEABLE":
        print(f'- [#{pr["number"]}]({pr["url"]})')
