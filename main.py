import json
import pymongo
import threading

from datetime import datetime
start_time = datetime.now()
'''
I've implemented this to compare execution times to know whether the threading actually improves anything
'''


def get_name(data):
    """
        finds and returns the name of the container
    :param data: data to be parsed
    :return: name of the lxc container
    """
    return data.get("name")


def get_cpu_usage(data):
    """
        finds and returns the cpu usage of the lxc container
    :param data: data to be parsed
    :return: cpu usage value, if the lxc container is not running, returns 0
    """
    try:
        return data["state"]["cpu"].get("usage")
    except TypeError:
        return 0
    
    
def get_memory_usage(data):
    """
        finds and returns memory usage of the lxc container
    :param data: data to be parsed
    :return: memory usage value, if the lxc container is not running, returns 0
    """
    try:
        return data["state"]["memory"].get("usage")
    except TypeError:
        return 0
    

def get_status(data):
    """
        finds and returns the status of the lxc container
    :param data: data to be parsed
    :return: status of the lxc container
    """
    return data.get("status")


def get_created_at(data):
    """
        finds and returns UTC timestamp of lxc container creation
    :param data: data to be parsed
    :return: UTC timestamp of lxc container creation converted from UTC datetime,
             the conversion is done through datetime module
    """
    return datetime.timestamp(datetime.strptime(data.get("created_at"), "%Y-%m-%dT%H:%M:%S%z"))


def get_ip_addresses(data):
    """
        finds and returns all the assigned IP addresses as a list
    :param data: data to be parsed
    :return: a list of all assigned IP addresses,
             if there are none, returns a message "No assigned IP addresses"
    """
    try:
        list_of_keys = list(data["state"]["network"].keys())
        ip_addresses = []
        for j in range(len(list_of_keys)):
            for k in range(len(data["state"]["network"][list_of_keys[j]]["addresses"])):
                try:
                    ip_addresses.append(data["state"]["network"][list_of_keys[j]]["addresses"][k]["address"])
                except TypeError:
                    continue
                except IndexError:
                    ip_addresses.append(data["state"]["network"][list_of_keys[j]]["addresses"]["address"])
                    break
        return ip_addresses
    except TypeError:
        return "No assigned IP addresses"


def parse_extract_upload(data, database):
    """
        parses through each lxc container at a time and sends the output containg name, cpu and memorz usage,
        status, date of creation and all assigned IP addresses in a list to the set database
    :param data: data to be parsed
    :param database: target database for the output
    """
    for i in range(len(data)):
        post = dict()

        post['name'] = get_name(data[i])
        post['cpu usage'] = get_cpu_usage(data[i])
        post['memory usage'] = get_memory_usage(data[i])
        post['status'] = get_status(data[i])
        post['created_at'] = get_created_at(data[i])
        post['assigned IP addresses'] = get_ip_addresses(data[i])

        # print(post)
        database.insert_one(post)


def main():
    file = open("sample-data.json", "r")
    loaded_data = json.load(file)

    mongodblink = input('Paste a link to the MongoDB db you want the output to be sent to:')
    cluster = pymongo.MongoClient(mongodblink)
    db = cluster['test_database']
    col = db["test_output"]
    x = threading.Thread(target=parse_extract_upload, args=(loaded_data, col))
    x.start()


if __name__ == '__main__':
    main()

end_time = datetime.now()
print('\nExecution time: {}'.format(end_time - start_time))
