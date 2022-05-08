from tgtg import TgtgClient
import json
with open("email", 'r') as f:
    email = f.readline()
client = TgtgClient(email=email)
credentials = client.get_credentials()
with open("tg.token", "w") as f:
    json.dump(credentials, f)

