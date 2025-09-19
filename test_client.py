import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print("✅ متصل به سرور!")

@sio.event
def disconnect():
    print("❌ قطع ارتباط")

@sio.event
def room_created(data):
    print(f"🎉 اتاق ایجاد شد: {data['room_id']}")
    print(f"👥 بازیکنان: {data['players']}")

@sio.event
def player_joined(data):
    print(f"🎯 بازیکن پیوست: {data['player_name']}")
    print(f"👥 بازیکنان: {data['players']}")

@sio.event
def game_started(data):
    print("🚀 بازی شروع شد!")
    print(f"👥 بازیکنان: {data['players']}")

@sio.event
def error(data):
    print(f"❌ خطا: {data['message']}")

def main():
    try:
        print("🔗 در حال اتصال به سرور...")
        sio.connect('http://127.0.0.1:5000')
        
        # تست ایجاد اتاق
        room_id = "test_room"
        player_name = "Player1"
        
        print(f"\n🎯 ایجاد اتاق: {room_id}")
        sio.emit('create_room', {
            'room_id': room_id,
            'player_name': player_name
        })
        
        # نگه داشتن اتصال
        print("\n⏳ در حال اجرا... (Ctrl+C برای خروج)")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 خروج از برنامه")
    except Exception as e:
        print(f"❌ خطا: {e}")
    finally:
        sio.disconnect()

if __name__ == '__main__':
    main()
