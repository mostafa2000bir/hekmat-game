from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
import random

class HekmatGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20
        
        # عنوان بازی
        self.title_label = Label(
            text="بازی حکم", 
            font_size=40,
            color=(1, 0.5, 0, 1)  # رنگ نارنجی
        )
        self.add_widget(self.title_label)
        
        # دکمه شروع بازی
        self.start_button = Button(
            text="شروع بازی جدید",
            size_hint=(1, 0.2),
            background_color=(0, 0.7, 0, 1)  # رنگ سبز
        )
        self.start_button.bind(on_press=self.start_game)
        self.add_widget(self.start_button)
        
        # وضعیت بازی
        self.status_label = Label(
            text="آماده برای شروع بازی...",
            font_size=20
        )
        self.add_widget(self.status_label)
    
    def start_game(self, instance):
        self.status_label.text = "بازی در حال اجرا است!\nدر حال آماده‌سازی کارت‌ها..."
        # بعداً اینجا لاژیک بازی رو اضافه می‌کنیم

class HekmatApp(App):
    def build(self):
        return HekmatGame()

if __name__ == '__main__':
    HekmatApp().run()
