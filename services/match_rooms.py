import argparse
import json
import time

from azure.storage import *


def get_loadfactor():
    if available_space == 0:
        return 1.0
    return occupied_spots/available_space

def new_room():
    return {"PartitionKey":course, "RowKey":str(int(time.time() * 1000)), "users": 0}


parser = argparse.ArgumentParser(description='Process a bunch of user requests.')
parser.add_argument('course', type=str, nargs=1,
                    help='the name of the class')
parser.add_argument('users', metavar='N', type=str, nargs='+',
                    help='a list of users looking for a room')

args = parser.parse_args()
course = args.course[0]

print course
print args.users

user_dicts = []
for user in args.users:
    user_dicts.append(eval(user))

myaccount = 'portalvhdskh6mzj3bsksr4'
mykey = '7adiqZaar7LYZmaFkLk4HnOuAuw+PlY8i8WNLTjYLOPNJvNe3ypn5nh6GYRw6akhsAjlFkJuEDzxtr3sk7JCrA=='

blob_service = BlobService(account_name=myaccount, account_key=mykey)
queue_service = QueueService(account_name=myaccount, account_key=mykey)
table_service = TableService(account_name=myaccount, account_key=mykey)

queue_service.create_queue("sendusers")

table_service.create_table("roomtable")

print course
rooms = table_service.query_entities("roomtable", "PartitionKey eq '{0}'".format(course))

occupied_spots = 0
for room in rooms:
    print room
    occupied_spots += room.users

room_to_users = dict((room.RowKey, room.users) for room in rooms)

available_space = len(rooms) * 6.0

response_dict = {}

for user in user_dicts:
    if get_loadfactor() > 0.8:
        new_room = new_room()
        table_service.insert_entity('roomtable', new_room)
        room_to_users[new_room['RowKey']] = 0
    room_key = min(room_to_users, key=room_to_users.get)
    response_dict[user['id']] = room_key
    room_to_users[room_key] += 1

print '{0}'.format(response_dict)
messages = queue_service.put_message('sendusers', '{0}'.format(response_dict))
