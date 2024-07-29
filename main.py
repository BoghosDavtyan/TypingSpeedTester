from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from random_word import RandomWords
import time


class FocusTextInput(TextInput):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'enter':
            self.dispatch('on_text_validate')
            return True
        return super(FocusTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)


class TypeTestApp(App):
    def build(self):
        self.r = RandomWords()
        self.current_word = ""
        self.time_left = 60
        self.words_typed = 0
        self.accuracy = 100
        self.game_active = False
        self.start_time = 0
        self.wpm = 0

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.time_label = Label(text=f"Time left: {self.time_left} seconds")
        layout.add_widget(self.time_label)

        self.word_label = Label(text="Press 'Start' to begin", font_size=30)
        layout.add_widget(self.word_label)

        self.input = FocusTextInput(multiline=False, font_size=30, disabled=True)
        self.input.bind(on_text_validate=self.check_word)
        layout.add_widget(self.input)

        self.start_button = Button(text="Start", on_press=self.start_game)
        layout.add_widget(self.start_button)

        self.stats_label = Label(text="Words typed: 0 | Accuracy: 100% | WPM: 0")
        layout.add_widget(self.stats_label)

        return layout

    def start_game(self, instance):
        self.start_button.disabled = True
        self.input.disabled = False
        self.input.focus = True
        self.time_left = 60
        self.words_typed = 0
        self.accuracy = 100
        self.wpm = 0
        self.game_active = True
        self.start_time = time.time()
        self.next_word()
        Clock.schedule_interval(self.update_timer, 1)

    def next_word(self):
        self.current_word = self.r.get_random_word()
        while not self.current_word:  # Ensure we get a valid word
            self.current_word = self.r.get_random_word()
        self.word_label.text = self.current_word

    def check_word(self, instance):
        if not self.game_active:
            return

        typed_word = self.input.text.strip().lower()
        if typed_word == self.current_word.lower():
            self.words_typed += 1
            self.input.text = ""
            self.next_word()
        else:
            self.accuracy = round((self.words_typed / (self.words_typed + 1)) * 100, 2)
            self.input.text = ""
            self.blink_textinput()
        self.update_stats()
        Clock.schedule_once(lambda dt: setattr(self.input, 'focus', True), 0.1)

    def blink_textinput(self):
        original_background = self.input.background_color

        def blink(dt):
            self.input.background_color = [1, 0, 0,
                                           1] if self.input.background_color == original_background else original_background

        for i in range(6):  # Blink 3 times (6 color changes)
            Clock.schedule_once(blink, i * 0.2)
        Clock.schedule_once(lambda dt: setattr(self.input, 'background_color', original_background), 1.2)

    def update_timer(self, dt):
        self.time_left -= 1
        self.time_label.text = f"Time left: {self.time_left} seconds"
        self.update_wpm()
        if self.time_left <= 0:
            self.end_game()
            return False
        return True

    def update_stats(self):
        self.update_wpm()
        self.stats_label.text = f"Words typed: {self.words_typed} | Accuracy: {self.accuracy}% | WPM: {self.wpm}"

    def update_wpm(self):
        elapsed_time = time.time() - self.start_time
        minutes = elapsed_time / 60
        self.wpm = round(self.words_typed / minutes, 2) if minutes > 0 else 0

    def end_game(self):
        self.game_active = False
        self.input.disabled = True
        self.word_label.text = "Game Over!"
        self.start_button.disabled = False
        self.start_button.text = "Play Again"
        self.update_stats()


if __name__ == '__main__':
    TypeTestApp().run()