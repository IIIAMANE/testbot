from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock  # Импортируем Clock для планирования задач в основном потоке
import requests
import time
from threading import Thread

class MainApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.user_spinner = Spinner(
            text="Select User ID",
            values=(),
            size_hint=(1, 0.2)
        )
        self.user_spinner.bind(text=self.load_messages)

        self.messages_scroll = ScrollView(size_hint=(1, 0.6))
        self.messages_label = Label(
            text="No messages loaded.",
            size_hint_y=None,
            height=500,
            valign="top",
            halign="left"
        )
        self.messages_label.bind(size=self.messages_label.setter('text_size'))
        self.messages_scroll.add_widget(self.messages_label)

        self.message_input = TextInput(
            hint_text="Type your message here",
            multiline=True,
            size_hint=(1, 0.1)
        )

        self.send_button = Button(
            text="Send Message",
            size_hint=(1, 0.1)
        )
        self.send_button.bind(on_press=self.send_message)

        self.layout.add_widget(self.user_spinner)
        self.layout.add_widget(self.messages_scroll)
        self.layout.add_widget(self.message_input)
        self.layout.add_widget(self.send_button)

        self.load_user_ids()

        # Start polling for new users and messages
        self.start_user_polling()

        return self.layout

    def load_user_ids(self):
        try:
            response = requests.get("http://192.168.1.4:8000/users")
            if response.status_code == 200:
                user_ids = response.json()
                self.user_spinner.values = [str(uid) for uid in user_ids]
            else:
                self.messages_label.text = f"Error loading user IDs: {response.status_code}"
        except Exception as e:
            self.messages_label.text = f"Error: {str(e)}"

    def load_messages(self, spinner, user_id):
        if not user_id or user_id == "Select User ID":
            return

        def poll_messages():
            last_timestamp = None
            while True:
                try:
                    params = {"since": last_timestamp} if last_timestamp else {}
                    response = requests.get(f"http://192.168.1.4:8000/messages/{user_id}", params=params)
                    if response.status_code == 200:
                        messages = response.json()
                        if messages:
                            last_timestamp = messages[-1]["timestamp"]
                            new_messages = "\n".join(
                                [f"[{msg['timestamp']}] {msg['text']}" for msg in messages]
                            )
                            # Используем Clock.schedule_once для обновления UI в основном потоке
                            Clock.schedule_once(lambda dt: self.update_messages(new_messages))
                    else:
                        self.messages_label.text = f"Error loading messages: {response.status_code}"
                except Exception as e:
                    self.messages_label.text = f"Error: {str(e)}"

                time.sleep(2)  # Poll every 2 seconds (you can adjust this)

        # Run polling in a separate thread to avoid blocking the main UI
        Thread(target=poll_messages, daemon=True).start()

    def update_messages(self, new_messages):
        """ Обновляет текст метки с новыми сообщениями """
        self.messages_label.text = new_messages

    def send_message(self, instance):
        user_id = self.user_spinner.text
        message = self.message_input.text

        if not user_id or user_id == "Select User ID":
            self.messages_label.text = "Please select a user ID."
            return

        if not message:
            self.messages_label.text = "Message cannot be empty."
            return

        try:
            response = requests.post(
                "http://192.168.1.4:8000/send_message",
                json={"user_id": int(user_id), "message": message}
            )

            if response.status_code == 200:
                self.messages_label.text = "Message sent successfully!"
                self.message_input.text = ""
            else:
                self.messages_label.text = f"Error sending message: {response.status_code}"
        except Exception as e:
            self.messages_label.text = f"Error: {str(e)}"

    def start_user_polling(self):
        """ Start polling for new users in the background """
        def poll_users():
            previous_user_ids = set()  # Сохраняем предыдущий список пользователей
            while True:
                try:
                    response = requests.get("http://192.168.1.4:8000/users")
                    if response.status_code == 200:
                        user_ids = response.json()
                        user_ids_set = set(user_ids)  # Преобразуем список в множество для быстрого сравнения
                        
                        # Если новый список пользователей отличается от предыдущего
                        if user_ids_set != previous_user_ids:
                            previous_user_ids = user_ids_set
                            # Обновляем список пользователей в спиннере
                            Clock.schedule_once(lambda dt: self.update_user_spinner(user_ids))
                    else:
                        self.messages_label.text = f"Error loading user IDs: {response.status_code}"
                except Exception as e:
                    self.messages_label.text = f"Error: {str(e)}"

                time.sleep(5)  # Poll every 5 seconds (you can adjust this)

        # Run polling in a separate thread to avoid blocking the main UI
        Thread(target=poll_users, daemon=True).start()

    def update_user_spinner(self, user_ids):
        """ Обновляет значения в спиннере пользователей, если они изменились """
        self.user_spinner.values = [str(uid) for uid in user_ids]

if __name__ == "__main__":
    MainApp().run()
