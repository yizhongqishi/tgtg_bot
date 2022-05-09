from tgtg import TgtgClient
import json
import time
from pprint import pprint
import telegram
import os
with open("tg.token", "r") as f:
    data = json.load(f)

client = TgtgClient(access_token=data["access_token"], refresh_token=data["refresh_token"], user_id=data["user_id"])
items = client.get_items()
for item in items:
    if item['items_available'] > 0:
        print("{}, {}".format(item["display_name"], item["item"]["item_id"]))
# while True:
#     try:
#         item = client.get_item(600644)
#         if item['items_available'] > 0:
#             print("New things, hurry up!")
#             # call me
#             pass
#         else:
#             print("Sleeping")
#             time.sleep(60)
#     except Exception as e:
#         print("error!")

