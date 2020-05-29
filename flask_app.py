from datetime import datetime
import random

from bson.json_util import dumps
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, join_room, leave_room
from pymongo.errors import DuplicateKeyError

from db import get_user, save_user, save_room, add_room_members, get_rooms_for_user, get_room, is_room_member, \
    get_room_members, is_room_admin, update_room, remove_room_members, save_message, get_messages, get_words, \
    add_room_member, save_clue

app = Flask(__name__)
app.secret_key = "sfdjkafnk"
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
def home():
    rooms = []
    if current_user.is_authenticated:
        rooms = get_rooms_for_user(current_user.username)
    return render_template("index.html", rooms=rooms)


@app.route('/login', methods=['GET', 'POST'])
def login():

    #save_images()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = 'Failed to login!'
    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            save_user(username, email, password)
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = "User already exists!"
    return render_template('signup.html', message=message)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# @app.route('/file/')
# def file():
#     image = get_image()
#     response = make_response(image.read())
#     response.mimetype = image.content_type
#     return response
#     #return dumps(image)

@app.route('/create-room/', methods=['GET', 'POST'])
@login_required
def create_room():
    message = ''
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        redusernames = [username.strip() for username in request.form.get('redmembers').split(',')]
        redSpy = request.form.get('redspymaster')
        blueusernames = [username.strip() for username in request.form.get('bluemembers').split(',')]
        blueSpy = request.form.get('bluespymaster')
        room_id = ''
        if blueSpy in blueusernames:
            blueusernames.remove(blueSpy)
        if redSpy in redusernames:
            redusernames.remove(redSpy)
        if len(room_name):
            if current_user.username == redSpy:
                room_id = save_room(room_name, current_user.username, 'red', True)
                add_room_member(room_id, room_name, blueSpy,redSpy,'False', 'blue', True)
            elif current_user.username == blueSpy:
                room_id = save_room(room_name, current_user.username, 'blue', True)
                add_room_member(room_id, room_name, redSpy, blueSpy,'False', 'red', True)
            else:

                if current_user.username in redusernames:
                    if not room_id:
                        room_id = save_room(room_name, current_user.username, 'red', False)
                        redusernames.remove(current_user.username)
                elif current_user.username in blueusernames:
                    if not room_id:
                        room_id = save_room(room_name, current_user.username, 'red', False)
                        blueusernames.remove(current_user.username)
                add_room_member(room_id, room_name, redSpy, current_user.username, 'False', 'red', True)
                add_room_member(room_id, room_name, blueSpy, current_user.username, 'False','blue', True)
            if len(redusernames):
                add_room_members(room_id, room_name, redusernames, current_user.username, 'red', False)
            if len(blueusernames):
                add_room_members(room_id, room_name, blueusernames, current_user.username, 'blue', False)
        else:
            message = "Failed to create room"

        return redirect(url_for('view_room', room_id=room_id,blueSpy=blueSpy,redSpy=redSpy))


    return render_template('create_room.html', message=message)


@app.route('/rooms/<room_id>/')
@login_required
def view_room(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        room_members = get_room_members(room_id)
        messages = get_messages(room_id)

        flash('You are in the game room!')
        return render_template('view_room.html', username=current_user.username, room=room, room_members=room_members,
                               messages=messages)
    else:
        return "Room not found", 404



@app.route('/rooms/<room_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    room = get_room(room_id)
    if room and is_room_admin(room_id, current_user.username):
        existing_room_members = [member['_id']['username'] for member in get_room_members(room_id)]
        room_members_str = ",".join(existing_room_members)
        message = ''
        if request.method == 'POST':
            room_name = request.form.get('room_name')
            room['name'] = room_name
            update_room(room_id, room_name)

            new_members = [username.strip() for username in request.form.get('members').split(',')]
            members_to_add = list(set(new_members) - set(existing_room_members))
            members_to_remove = list(set(existing_room_members) - set(new_members))
            if len(members_to_add):
                add_room_members(room_id, room_name, members_to_add, current_user.username)
            if len(members_to_remove):
                remove_room_members(room_id, members_to_remove)
            message = 'Room edited successfully'
            room_members_str = ",".join(new_members)
        return render_template('edit_room.html', room=room, room_members_str=room_members_str, message=message)
    else:
        return "Room not found", 404



@app.route('/rooms/<room_id>/messages/')
@login_required
def get_older_messages(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        page = int(request.args.get('page', 0))
        messages = get_messages(room_id, page)
        return dumps(messages)
    else:
        return "Room not found", 404

@app.route('/rooms/<room_id>/board/')
@login_required
def create_board(room_id):

    with open('nounlist.txt') as f:
        lines = f.read().splitlines()
    random.shuffle(lines)

    #board = get_words()
    #add board to DB with room_id

    return dumps(lines[:20])


@app.route('/rooms/<room_id>/board_clue/')
@login_required
def create_board_clue(room_id):
    board = []
    blue , red, normal = 7,7,4
    for i in range(20):
            if blue:
                board.append('blue')
                blue -= 1
            elif red:
                board.append('red')
                red -= 1
            elif normal:
                board.append('neutral')
                normal -= 1
            else:
                break
    board.append('bomb')
    if random.randint(0,1): #extrablue
        board.append('blue')
    else:
        board.append('red')
    random.shuffle(board)
    #add boardclue to database
    return dumps(board)




@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    save_message(data['room'], data['message'], data['username'])
    socketio.emit('receive_message', data, room=data['room'])
@socketio.on('send_clue')
def handle_send_clue_event(data):
    app.logger.info("{} has sent clue to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['clue']))
    data['color'] = save_clue(data['room'], data['clue'], data['username'])

    socketio.emit('receive_clue', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


@login_manager.user_loader
def load_user(username):
    return get_user(username)


if __name__ == '__main__':
    socketio.run(app, debug=True)