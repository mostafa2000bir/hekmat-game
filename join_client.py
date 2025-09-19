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
def player_joined(data):
    print(f"🎯 بازیکن پیوست: {data['player_name']}")
    print(f"👥 بازیکنان: {data['players']}")

@sio.event
def error(data):
    print(f"❌ خطا: {data['message']}")

def main():
    try:
        print("🔗 در حال اتصال به سرور...")
        sio.connect('http://127.0.0.1:5000')
        
        # پیوستن به اتاق موجود
        room_id = "test_room"  # همان اتاق قبلی
        player_name = "Player2"  # نام متفاوت
        
        print(f"\n🎯 پیوستن به اتاق: {room_id}")
        sio.emit('join_room', {
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
