import json

with open('Examples/UpstreamExample.json') as json_file:
    data = json.load(json_file)
    # print(data)
    #Get groups list
    print("Groups list")
    print(data['groups'])
    print("particular group")
    print(data['work'])
    print("tasks list")
    print(data['work']['tasks'])
    print("tasks info")
    print(data['work']['coding'])
