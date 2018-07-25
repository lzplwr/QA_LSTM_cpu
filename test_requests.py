# -*- coding: utf-8 -*-

import requests

url = "http://127.0.0.1:9008/api"
data = {
    "sentence":"头像是什么"
}


response = requests.post(url=url, data=data)
print(response.text)