import json
import pymongo

from datetime import datetime
start_time = datetime.now()
'''
To compare runtime of the code
'''

file = open("sample-data.json", "r")

MongoDBlink = input('Paste a link to the MongoDB db:')
cluster = pymongo.MongoClient(MongoDBlink)
db = cluster['test_database']
col = db["test_output"]

data = json.load(file)

for i in range(len(data)):
    post = dict()
    post['name'] = data[i].get("name")
    try:
        post['cpu usage'] = data[i]["state"]["cpu"].get("usage")
    except TypeError:
        post['cpu usage'] = 0

    try:
        post['memory usage'] = data[i]["state"]["memory"].get("usage")
    except TypeError:
        post['memory usage'] = 0

    post['status'] = data[i].get("status")

    post['created_at'] = data[i].get("created_at")

    try:
        list_of_keys = list(data[i]["state"]["network"].keys())
        ip_addresses = []
        for j in range(len(list_of_keys)):
            for k in range(len(data[i]["state"]["network"][list_of_keys[j]]["addresses"])):
                try:
                    ip_addresses.append(data[i]["state"]["network"][list_of_keys[j]]["addresses"][k]["address"])
                except TypeError:
                    continue
                except IndexError:
                    ip_addresses.append(data[i]["state"]["network"][list_of_keys[j]]["addresses"]["address"])
                    break
        post['assigned IP addressses'] = ip_addresses
    except TypeError:
        post['assigned IP addressses'] = "No assigned IP addresses"

    col.insert_one(post)


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))
