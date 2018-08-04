# -*- coding: utf-8 -*-

import requests

url = "http://127.0.0.1:9008/api"
data = {
    "sentence":"心脏病保不保"
}


response = requests.post(url=url, data=data)
print(response.text.encode('utf-8').decode('unicode_escape'))