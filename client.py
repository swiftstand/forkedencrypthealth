#!/usr/bin/env python3
import sys
import requests
import pprint
import asyncio

# Get all
response = requests.get('http://localhost:10000/diagnosis')
pprint.pprint(response.json())

sys.exit()
# Get one
response = requests.get('http://localhost:10000/diagnosis/62411a91d459378394011d3e')
pprint.pprint(response.json())

# Create one
response = requests.post(
    'http://localhost:10000/diagnosis',
    json={
        "name": "From python",
        "labTests": "everything"
    }
)
pprint.pprint(response.json())
