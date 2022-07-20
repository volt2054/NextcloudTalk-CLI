import json
import requests
import time
import os

# Headers sent with request
headers = {'OCS-APIRequest': 'true',
           'Content-Type': 'application/json',
           'Accept': 'application/json'
           }

# Set paramaters for requesting chat messages, limit to 10 to make it fast for testing
data_chat = {'lookIntoFuture':0, 'setReadMarker': 0, 'limit':10}

# Specify cache directory
jsondir = "./cache"

# Try to load dictionary else create empty dict
# TODO: Problem if 2 convos have the same participant name
try:
    with open(f"{jsondir}/dictionary.json",'r') as lf:
        dict_token_participant= json.load(lf)
except:
    dict_token_participant = {}
