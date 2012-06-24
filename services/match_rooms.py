import argparse
import json
import time

from azure.storage import *
from tokbox import *


def get_loadfactor():
    print occupied_spots / available_space
    if available_space == 0:
        return 1.0
    return occupied_spots / available_space


def new_room():
    row_key = str(int(time.time() * 1000))
    etherpad = course + "_" + row_key
    return {"PartitionKey": course,
            "RowKey": row_key,
            "users": 0,
            "tokbox": create_session(),
            "etherpad": etherpad}


def create_new_room():
    """ Function for outside programs to call to easily create a new room. """
    new_room = new_room()


parser = argparse.ArgumentParser(description='Process a bunch of user requests.')
parser.add_argument('course', type=str, nargs=1,
                    help='the name of the class')
parser.add_argument('users', metavar='N', type=str, nargs='+',
                    help='a list of users looking for a room')

args = parser.parse_args()
course = args.course[0]

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

rooms = table_service.query_entities("roomtable", "PartitionKey eq '{0}'".format(course))

occupied_spots = 0
for room in rooms:
    occupied_spots += room.users

room_to_users = dict((room.RowKey, room.users) for room in rooms)

available_space = len(rooms) * 6.0

response_dict = {}

for user in user_dicts:
    print("Load factor: {0}".format(get_loadfactor()))
    if get_loadfactor() > 0.7:
        n_room = new_room()
        print "Creating new room..."
        print (n_room)
        table_service.insert_entity('roomtable', n_room)
        available_space += 6.0
        room_to_users[n_room['RowKey']] = 0

    room_key = min(room_to_users, key=room_to_users.get)
    response_dict[user['id']] = room_key
    room_to_users[room_key] += 1
    occupied_spots += 1

print(response_dict)
messages = queue_service.put_message('sendusers', str(response_dict))


rooms = table_service.query_entities("roomtable", "PartitionKey eq '{0}'".format(course))

for row_key in room_to_users.keys():
    row = table_service.get_entity('roomtable', str(course), str(row_key))
    row.users += 1
    table_service.update_entity('roomtable', str(course), str(row_key), row)
