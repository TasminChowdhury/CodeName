from datetime import datetime
import gridfs
from bson import ObjectId
from pymongo import MongoClient, DESCENDING
from werkzeug.security import generate_password_hash

from user import User
client = MongoClient("mongodb+srv://ChatApp:ChatApp@chatapp-t7gml.mongodb.net/test?retryWrites=true&w=majority")

chat_db = client.get_database("ChatAppDB")
users_collection = chat_db.get_collection("users")
rooms_collection = chat_db.get_collection("rooms")
room_members_collection = chat_db.get_collection("room_members")
messages_collection = chat_db.get_collection("messages")
clue_collection = chat_db.get_collection("clue")
word_collection = chat_db.get_collection("words")
image_id = []
fs = gridfs.GridFS(chat_db)
# def get_image():
#     outputdata = fs.get(image_id[0])
#     return outputdata
# def save_images():
#
#     datafile = open("C:\clue.jpg", "rb");
#
#     thedata = datafile.read()
#     # store the data in the database. Returns the id of the file in gridFS
#     stored = fs.put(thedata, filename="testimage")
#     image_id.append(stored)
#     # retrieve what was just stored.
#     #outputdata = fs.get(stored).read()

def save_user(username, email, password):
    password_hash = generate_password_hash(password)
    users_collection.insert_one({'_id': username, 'email': email, 'password': password_hash})


def get_user(username):
    user_data = users_collection.find_one({'_id': username})
    return User(user_data['_id'], user_data['email'], user_data['password']) if user_data else None


def save_room(room_name, created_by,color,spy):
    room_id = rooms_collection.insert_one(
        {'name': room_name, 'created_by': created_by, 'created_at': datetime.now()}).inserted_id
    add_room_member(room_id, room_name, created_by, created_by,True, color, spy)
    return room_id


def update_room(room_id, room_name):
    rooms_collection.update_one({'_id': ObjectId(room_id)}, {'$set': {'name': room_name}})
    room_members_collection.update_many({'_id.room_id': ObjectId(room_id)}, {'$set': {'room_name': room_name}})


def get_room(room_id):
    return rooms_collection.find_one({'_id': ObjectId(room_id)})


def add_room_member(room_id, room_name, username, added_by, is_room_admin, color ,spy):
    room_members_collection.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin, 'color': color, 'is_spy_master': spy})


def add_room_members(room_id, room_name, usernames, added_by, color,spy):
    room_members_collection.insert_many(
        [{'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
          'added_at': datetime.now(), 'is_room_admin': False, 'color': color, 'is_spy_master': spy} for username in usernames])


def remove_room_members(room_id, usernames):
    room_members_collection.delete_many(
        {'_id': {'$in': [{'room_id': ObjectId(room_id), 'username': username} for username in usernames]}})


def get_room_members(room_id):
    return list(room_members_collection.find({'_id.room_id': ObjectId(room_id)}))


def get_rooms_for_user(username):
    return list(room_members_collection.find({'_id.username': username}))


def is_room_member(room_id, username):
    return room_members_collection.count_documents({'_id': {'room_id': ObjectId(room_id), 'username': username}})


def is_room_admin(room_id, username):
    return room_members_collection.count_documents(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'is_room_admin': True})


def save_message(room_id, text, sender):
    messages_collection.insert_one({'room_id': room_id, 'text': text, 'sender': sender, 'created_at': datetime.now()})

def save_clue(room_id, clue, sender):
    # print(room_id, clue, sender)
    temp= room_members_collection.find_one({'_id': {'room_id': ObjectId(room_id), 'username': sender}}, {'color':1})
    #print('print the color of the sender', temp['color'])
    clue_collection.insert_one({'room_id': room_id, 'clue': clue, 'sender': sender,'color': temp['color']})
    return temp['color']

MESSAGE_FETCH_LIMIT = 3


def get_messages(room_id, page=0):
    offset = page * MESSAGE_FETCH_LIMIT
    messages = list(
        messages_collection.find({'room_id': room_id}).sort('_id', DESCENDING).limit(MESSAGE_FETCH_LIMIT).skip(offset))
    for message in messages:
        message['created_at'] = message['created_at'].strftime("%d %b, %H:%M")
    return messages[::-1]

def save_words(word):
    word_collection.insert_one({'word': word, 'created_at': datetime.now()})
WORD_FETCH_LIMIT = 20
def get_words():
    words = list(word_collection.find( { } ).limit(WORD_FETCH_LIMIT))
    return words


# def save_imgs(word):
#     word_collection.insert_one({'word': word, 'created_at': datetime.now()})
# WORD_FETCH_LIMIT = 20
# def get_words():
#     words = list(word_collection.find( { } ).limit(WORD_FETCH_LIMIT))
#     return words