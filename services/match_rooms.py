import argparse
import json

from azure.storage import *


parser = argparse.ArgumentParser(description='Process a bunch of user requests.')
parser.add_argument('course', type=str, nargs=1,
                    help='the name of the class')
parser.add_argument('users', metavar='N', type=str, nargs='+',
                    help='a list of users looking for a room')

args = parser.parse_args()

course = args.course
user_dicts = []
for user in args.user:
    user_dicts.append(json.loads(user))

myaccount = 'portalvhdskh6mzj3bsksr4'
mykey = '7adiqZaar7LYZmaFkLk4HnOuAuw+PlY8i8WNLTjYLOPNJvNe3ypn5nh6GYRw6akhsAjlFkJuEDzxtr3sk7JCrA=='

blob_service = BlobService(account_name=myaccount, account_key=mykey)
queue_service = QueueService(account_name=myaccount, account_key=mykey)
table_service = TableService(account_name=myaccount, account_key=mykey)

queue_service.create_queue('send_users')

rooms_tablename = course + 'rooms'
table_service.create_table(tablename)

rooms = table_service.query_entities(rooms_tablename, "PartitionKey eq {0}".format(course))
for room in rooms:
    occupied_spots += room.users

room_to_users = dict((room['RowKey'], room['users']) for room in rooms)

occupied_spots = 0
available_space = len(rooms) * 6.0

response_dict = {}

for user in user_dicts:
    if get_loadfactor() > 0.8:
        new_room = new_room()
        table_service.put_message(rooms_tablename, new_room())
        room_to_users[new_room['RowKey']] = 0
    room_key = min(room_to_users, key=room_to_users.get)
    response_dict[user['id']] = room_key
    room_to_users[room_key] += 1

messages = queue_service.put_message('send_users', str(response_dict))

for message in messages:
    process(message)
    queue_service.delete_message('taskqueue', message.message_id, message.pop_receipt)

def get_loadfactor():
    if available_space = 0
        return 1.0
    return occupied_spots/available_space

def new_room():
    return {"PartitionKey":course, "RowKey":int(time.time() * 1000), "users": "[]"}
