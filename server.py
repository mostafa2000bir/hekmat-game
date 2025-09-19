from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hekmat_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# ذخیره‌سازی داده‌های بازی
rooms = {}
players = {}

@socketio.on('connect')
def handle_connect():
    print('یک کلاینت متصل شد')
    emit('connected', {'message': 'به سرور حکم خوش آمدید!'})

@socketio.on('create_room')
def handle_create_room(data):
    room_id = data.get('room_id')
    player_name = data.get('player_name')
    
    if not room_id or not player_name:
        emit('error', {'message': 'شناسه اتاق یا نام بازیکن وجود ندارد'})
        return
    
    rooms[room_id] = {
        'players': [player_name],
        'game_state': 'waiting',
        'cards': [],
        'scores': {player_name: 0}
    }
    
    players[player_name] = room_id
    join_room(room_id)
    
    emit('room_created', {
        'room_id': room_id,
        'players': rooms[room_id]['players']
    }, room=room_id)
    
    print(f'اتاق {room_id} توسط {player_name} ایجاد شد')

@socketio.on('join_room')
def handle_join_room(data):
    room_id = data.get('room_id')
    player_name = data.get('player_name')
    
    if not room_id or not player_name:
        emit('error', {'message': 'شناسه اتاق یا نام بازیکن وجود ندارد'})
        return
    
    if room_id not in rooms:
        emit('error', {'message': 'اتاق پیدا نشد'})
        return
    
    if player_name in rooms[room_id]['players']:
        emit('error', {'message': 'این نام قبلاً استفاده شده'})
        return
    
    rooms[room_id]['players'].append(player_name)
    rooms[room_id]['scores'][player_name] = 0
    players[player_name] = room_id
    join_room(room_id)
    
    emit('player_joined', {
        'player_name': player_name,
        'players': rooms[room_id]['players']
    }, room=room_id)
    
    print(f'{player_name} به اتاق {room_id} پیوست')

@socketio.on('start_game')
def handle_start_game(data):
    room_id = data.get('room_id')
    
    if room_id not in rooms:
        emit('error', {'message': 'اتاق پیدا نشد'})
        return
    
    rooms[room_id]['game_state'] = 'playing'
    
    # توزیع کارت‌ها (اینجا می‌تونیم منطق کامل رو اضافه کنیم)
    emit('game_started', {
        'message': 'بازی شروع شد!',
        'players': rooms[room_id]['players']
    }, room=room_id)
    
    print(f'بازی در اتاق {room_id} شروع شد')

if __name__ == '__main__':
    print('🚀 سرور بازی حکم در حال اجرا روی پورت 5000...')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
