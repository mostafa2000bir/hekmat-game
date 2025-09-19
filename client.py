import socketio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

sio = socketio.Client()

class HekmatClient(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20
        
        self.status_label = Label(text="وضعیت: قطع ارتباط", size_hint=(1, 0.2))
        self.add_widget(self.status_label)
        
        self.room_id_input = TextInput(hint_text="شناسه اتاق", size_hint=(1, 0.1))
        self.add_widget(self.room_id_input)
        
        self.name_input = TextInput(hint_text="نام بازیکن", size_hint=(1, 0.1))
        self.add_widget(self.name_input)
        
        self.connect_btn = Button(text="اتصال به سرور", size_hint=(1, 0.1))
        self.connect_btn.bind(on_press=self.connect_to_server)
        self.add_widget(self.connect_btn)
        
        self.create_btn = Button(text="ایجاد اتاق", size_hint=(1, 0.1))
        self.create_btn.bind(on_press=self.create_room)
        self.add_widget(self.create_btn)
        
        self.join_btn = Button(text="پیوستن به اتاق", size_hint=(1, 0.1))
        self.join_btn.bind(on_press=self.join_room)
        self.add_widget(self.join_btn)
        
        self.start_btn = Button(text="شروع بازی", size_hint=(1, 0.1))
        self.start_btn.bind(on_press=self.start_game)
        self.add_widget(self.start_btn)
        
        # تنظیم event handlers
        sio.on('connect', self.on_connect)
        sio.on('disconnect', self.on_disconnect)
        sio.on('room_created', self.on_room_created)
        sio.on('player_joined', self.on_player_joined)
        sio.on('game_started', self.on_game_started)
        sio.on('error', self.on_error)

    def connect_to_server(self, instance):
        try:
            sio.connect('http://127.0.0.1:5000')
            self.status_label.text = "در حال اتصال..."
        except Exception as e:
            self.status_label.text = f"خطا: {str(e)}"

    def create_room(self, instance):
        room_id = self.room_id_input.text
        player_name = self.name_input.text
        if room_id and player_name:
            sio.emit('create_room', {
                'room_id': room_id,
                'player_name': player_name
            })
        else:
            self.status_label.text = "لطفاً شناسه اتاق و نام را وارد کنید"

    def join_room(self, instance):
        room_id = self.room_id_input.text
        player_name = self.name_input.text
        if room_id and player_name:
            sio.emit('join_room', {
                'room_id': room_id,
                'player_name': player_name
            })
        else:
            self.status_label.text = "لطفاً شناسه اتاق و نام را وارد کنید"

    def start_game(self, instance):
        room_id = self.room_id_input.text
        if room_id:
            sio.emit('start_game', {'room_id': room_id})

    # Event handlers
    def on_connect(self):
        self.status_label.text = "متصل به سرور!"

    def on_disconnect(self):
        self.status_label.text = "قطع ارتباط"

    def on_room_created(self, data):
        self.status_label.text = f"اتاق {data['room_id']} ایجاد شد"

    def on_player_joined(self, data):
        self.status_label.text = f"{data['player_name']} پیوست"

    def on_game_started(self, data):
        self.status_label.text = "بازی شروع شد!"

    def on_error(self, data):
        self.status_label.text = f"خطا: {data['message']}"

class HekmatApp(App):
    def build(self):
        return Hekmat
