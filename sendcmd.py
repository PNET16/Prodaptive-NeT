#!/usr/bin/env python
import requests
import json

url = 'http://127.0.0.1:8080/myswitch/cmd/2'
payload = {'cmd': '2'}
ip_src = raw_input("IP addr => ")
payload["IP_SRC"]= ip_src
# Create your header as required
headers = {"content-type": "application/json", "Authorization": "<auth-key>" }

r = requests.put(url, data=json.dumps(payload), headers=headers)
