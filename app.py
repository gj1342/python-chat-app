from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
# This line ensures static files are served with the correct path
app.static_folder = 'static'
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    username = f'User{random.randint(1, 1000)}'
    gender = random.choice(['girl', 'boy'])
    
    # Use a different avatar service that's more reliable
    avatar_url = f'https://ui-avatars.com/api/?name={username}&background=random'
    
    users[request.sid] = {
        'username': username,
        'avatar': avatar_url,
        'gender': gender
    }
    
    emit('user_joined', {'username':username,'avatar':avatar_url},broadcast=True)
    
    emit('set_username', {'username':username})
    
@socketio.on('disconnect')
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
        emit('user_left', {'username':user['username']},broadcast=True)
        
@socketio.on('send_message')
def handle_send_message(data):
    user = users.get(request.sid)
    
    if user:
        emit('new_message', {
            'username':user['username'],
            'avatar':user['avatar'],  # Make sure this matches the key above
            'message':data['message'],
        },broadcast=True)

@socketio.on('update_username')
def handle_update_username(data):
    old_username = users[request.sid]['username']
    new_username = data['username']
    users[request.sid]['username'] = new_username
    
    emit('username_updated', {'old_username':old_username, 'new_username':new_username},broadcast=True)
        
if __name__ == '__main__':
    socketio.run(app)



