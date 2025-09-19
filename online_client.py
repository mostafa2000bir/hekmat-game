from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import socketio

class HekmatOnlineClient(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.sio = socketio.Client()
        self.setup_connection_handlers()
        
        # UI برای اتصال
        self.room_id_input = TextInput(hint_text='شناسه اتاق', size_hint=(1, 0.1))
        self.add_widget(self.room_id_input)
        
        self.connect_button = Button(text='اتصال به اتاق', size_hint=(1, 0.1))
        self.connect_button.bind(on_press=self.connect_to_room)
        self.add_widget(self.connect_button)
        
        self.status_label = Label(text='آماده برای اتصال...', size_hint=(1, 0.2))
        self.add_widget(self.status_label)

    def setup_connection_handlers(self):
        @self.sio.event
        def connect():
            self.status_label.text = 'متصل به سرور!'

        @self.sio.event
        def disconnect():
            self.status_label.text = 'قطع ارتباط!'

        @self.sio.event
        def room_created(data):
            self.status_label.text = f'اتاق ایجاد شد: {data["room_id"]}'

        @self.sio.event
        def player_joined(data):
            self.status_label.text = f'بازیکن پیوست: {data["player_name"]}'

    def connect_to_room(self, instance):
        room_id = self.room_id_input.text
        try:
            self.sio.connect('http://localhost:5000')
            self.sio.emit('join_room', {
                'room_id': room_id,
                'player_name': 'Player1'
            })
        except Exception as e:
            self.status_label.text = f'خطا: {str(e)}'

class HekmatOnlineApp(App):
    def build(self):
        return HekmatOnlineClient()

if __name__ == '__main__':
    HekmatOnlineApp().run()
