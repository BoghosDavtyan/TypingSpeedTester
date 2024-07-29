from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import random


class BlinkingTextInput(TextInput):
    def blink(self, dt):
        self.background_color = [1, 0, 0, 1] if self.background_color == [1, 1, 1, 1] else [1, 1, 1, 1]


class TypeTestApp(App):
    def build(self):
        self.words = ["python", "kivy", "application", "development", "programming", "computer", "science", "algorithm",
                      "interface", "software"]
        self.current_word = ""
        self.time_left = 60
        self.words_typed = 0
        self.accuracy = 100
        self.game_active = False

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.time_label = Label(text=f"Time left: {self.time_left} seconds")
        layout.add_widget(self.time_label)

        self.word_label = Label(text="Press 'Start' to begin", font_size=30)
        layout.add_widget(self.word_label)

        self.input = BlinkingTextInput(multiline=False, font_size=30, disabled=True)
        self.input.bind(on_text_validate=self.check_word)
        layout.add_widget(self.input)

        self.start_button = Button(text="Start", on_press=self.start_game)
        layout.add_widget(self.start_button)

        self.stats_label = Label(text="Words typed: 0 | Accuracy: 100%")
        layout.add_widget(self.stats_label)

        return layout

    def start_game(self, instance):
        self.start_button.disabled = True
        self.input.disabled = False
        self.input.focus = True
        self.time_left = 60
        self.words_typed = 0
        self.accuracy = 100
        self.game_active = True
        self.next_word()
        Clock.schedule_interval(self.update_timer, 1)

    def next_word(self):
        self.current_word = random.choice(self.words)
        self.word_label.text = self.current_word

    def check_word(self, instance):
        if not self.game_active:
            return

        typed_word = self.input.text.strip().lower()
        if typed_word == self.current_word:
            self.words_typed += 1
            self.input.text = ""
            self.next_word()
        else:
            self.accuracy = round((self.words_typed / (self.words_typed + 1)) * 100, 2)
            self.input.text = ""
            self.blink_textinput()
        self.update_stats()
        self.input.focus = True

    def blink_textinput(self):
        blink_count = 0

        def blink(dt):
            nonlocal blink_count
            self.input.blink(dt)
            blink_count += 1
            if blink_count >= 6:
                return False

        Clock.schedule_interval(blink, 0.2)

    def update_timer(self, dt):
        self.time_left -= 1
        self.time_label.text = f"Time left: {self.time_left} seconds"
        if self.time_left <= 0:
            self.end_game()
            return False
        return True

    def update_stats(self):
        self.stats_label.text = f"Words typed: {self.words_typed} | Accuracy: {self.accuracy}%"

    def end_game(self):
        self.game_active = False
        self.input.disabled = True
        self.word_label.text = "Game Over!"
        self.start_button.disabled = False
        self.start_button.text = "Play Again"


if __name__ == '__main__':
    TypeTestApp().run()