# ну ваще как будто аву можно парсить
# время сделать
# оценку состояния сделать в троеточии
# комменты чекнуть в троеточии
# фиксануть комм, где тест выходит за поле и поле, как в тг не увеличивается
# аватарки круглыми сделать

import os
from io import BytesIO
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.core.image import Image as CoreImage
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemSupportingText
from kivy.core.window import Window
from kivy.uix.image import Image

from kivymd.uix.label import MDLabel
import requests
from kivy.uix.screenmanager import ScreenManager, Screen

KV = '''
MDScreen:

# Экран выбора диалога, мейн
<Demo1>:
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            type: "small"
            
            MDTopAppBarLeadingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "menu"

            MDTopAppBarTitle:
                text: "Prikol"

            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "account-search"

        MDScrollView:
            do_scroll_x: False

            MDBoxLayout:
                id: main_scroll
                orientation: "vertical"
                adaptive_height: True

                MDList:
                    id: item_list

# Виджет, рисующий прямоугольник моего сообщения
<MyMessage>
    size_hint_y: None
    pos_hint: {"right": .98}
    height: self.texture_size[1]
    padding: 12, 10
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    canvas.before:
        Color:
            rgb: (42/255, 47/255, 51/255, 1)
        RoundedRectangle:
            size: self.width, self.height
            pos: self.pos
            radius: [23, 23, 0, 23]

# Виджет, рисующий прямоугольник сообщения собеседника
<Response>
    size_hint_y: None
    pos_hint: {"x": .02}
    height: self.texture_size[1]
    padding: 12, 10
    canvas.before:
        Color:
            rgb: (0/255,191/255,176/255,1)
        RoundedRectangle:
            size: self.width, self.height
            pos: self.pos
            radius: [23, 23, 23, 0]                  

# Экран чата
<Demo2>:
    BoxLayout:
        orientation: "vertical"

        # Верхняя панелька
        MDTopAppBar:
            type: "small"
            
            MDTopAppBarLeadingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "keyboard-backspace"
                    on_release: root.manager.current = "demo1"

            MDTopAppBarTitle:
                id: AppBarUserId
                text: "Prikol"

            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "dots-vertical"

        # Окно сообщений
        ScrollView:
            size_hint_y: .77
            do_scroll_x: False
            do_scroll_y: True
            BoxLayout:
                id: chat_list
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 5

        # Нижняя панелька
        MDFloatLayout:
            md_bg_color: 245/255, 245/255, 245/255, 1
            size_hint_y: .07

            MDFloatLayout:
                size_hint: .8, .75
                pos_hint: {"center_x": .43, "center_y": .5}
                canvas:
                    Color:
                        rgb: (238/255, 238/255, 238/255, 1)
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos
                        radius: [23, 23, 23, 23]

                TextInput:
                    id: text_input
                    hint_text: "Вводи сообщение..."
                    size_hint: 1, None
                    pos_hint: {"center_x": .5, "center_y": .5}
                    font_size: "18sp"
                    height: self.minimum_height
                    multiline: True                                  # Сделать адаптацию высоты поля под текст
                    cursor_color: 255/255, 100/255, 202/255, 1
                    cursor_width: "2sp"
                    foreground_color: 0/255, 0/255, 0/255, 1
                    background_color: 1, 1, 1, 0
                    padding: 15
                    
            MDIconButton:
                icon: "send"
                pos_hint: {"center_x": .91, "center_y": .5}
                user_font_size: "18sp"
                theme_text_color: "Custom"
                text_color: 255/255, 100/255, 202/255, 1
                md_bg_color: 255/255, 255/255, 255/255, 0
                on_release: app.send()
'''

id_list = requests.get("http://192.168.1.4:8000/users").json()

def get_user_avatar(user_id):
    token = os.getenv("TOKEN")
    
    # Запрос фотографий профиля
    response = requests.get(f"https://api.telegram.org/bot{token}/getUserProfilePhotos?user_id={user_id}")
    photos_data = response.json()
    
    if not photos_data.get("ok") or photos_data["result"]["total_count"] == 0:
        return None  # У пользователя нет аватарок
    
    # Извлекаем file_id первой аватарки
    file_id = photos_data["result"]["photos"][0][0]["file_id"]
    
    # Получаем информацию о файле
    file_response = requests.get(f"https://api.telegram.org/bot{token}/getFile?file_id={file_id}")
    file_data = file_response.json()
    
    if not file_data.get("ok"):
        return None  # Ошибка получения информации о файле
    
    # Формируем прямой URL к аватарке
    file_path = file_data["result"]["file_path"]
    avatar_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    
    return avatar_url


class MyMessage(MDLabel):
    font_size = 17

class Response(MDLabel):
    font_size = 17

class Demo1(Screen):
    def on_enter(self):
        item_list = self.ids.item_list

        if item_list.children:
            return

        for user_id in id_list:
            item = MDListItem()

            url_avatar = get_user_avatar(user_id)

            if url_avatar == None:
                image_path = "avatar.jpg"
                image = Image(source=image_path, size_hint=(None, None), size=(48, 48))

            elif url_avatar != None:
                response = requests.get(url_avatar)
                if response.status_code == 200:
                    data = BytesIO(response.content)
                    core_image = CoreImage(data, ext="jpg")  # Убедитесь, что формат соответствует загружаемому
                    image = Image(texture=core_image.texture, size_hint=(None, None), size=(48, 48))
                else:
                    # В случае ошибки используем изображение по умолчанию
                    image_path = "avatar.jpg"
                    image = Image(source=image_path, size_hint=(None, None), size=(48, 48))



            headline = MDListItemHeadlineText(text=f"{user_id}")
            supporting_line_text = MDListItemSupportingText(text="Последнее сообщение")

            item.on_release = lambda user_id = user_id: self.on_chat_click(user_id)

            item.add_widget(image)
            item.add_widget(headline)
            item.add_widget(supporting_line_text)

            item_list.add_widget(item)

    def on_chat_click(self, user_id):
        self.manager.current = "demo2"
        demo2_screen = self.manager.get_screen("demo2")
        demo2_screen.update_for_chat_screen(user_id)


class Demo2(Screen):
    def on_pre_enter(self, *args):
        """Запускает автообновление при входе на экран."""
        self.event = Clock.schedule_interval(self.update_chat, 5)  # Каждые 5 секунд

    def on_leave(self, *args):
        """Останавливает автообновление при выходе с экрана."""
        if hasattr(self, 'event'):
            self.event.cancel()

    def update_chat(self, dt):
        """Метод для обновления чата."""
        user_id = self.ids.AppBarUserId.text  # Получаем текущий user_id из AppBar
        self.update_for_chat_screen(user_id)

    def update_for_chat_screen(self, user_id):
        self.ids.AppBarUserId.text = f"{user_id}"
        self.ids.chat_list.clear_widgets()
        get_messages_request = requests.get(f"http://192.168.1.4:8000/messages/{user_id}")
        if get_messages_request.status_code == 200:
            for message in get_messages_request.json():
                print(message['id'], message['sender_type'], message['text'])
                text = message['text']
                if len(text) < 6:
                    size_hint_x = 0.18
                elif len(text) < 11:
                    size_hint_x = .3
                elif len(text) < 16:
                    size_hint_x = .4
                elif len(text) < 21:
                    size_hint_x = .5
                elif len(text) < 26:
                    size_hint_x = .65
                else:
                    size_hint_x = .75

                if message['sender_type'] == "bot":
                    message = MyMessage(
                        text=text,
                        size_hint_x=size_hint_x,
                        halign="right",
                        padding=(10, 10)
                    )
                    
                    self.ids.chat_list.add_widget(message)

                elif message['sender_type'] == "user":
                    message = Response(
                        text=text,
                        size_hint_x=size_hint_x,
                        halign="right",
                        padding=(10, 10)
                    )

                    self.ids.chat_list.add_widget(message)

class MainApp(MDApp):
    def build(self):
        Builder.load_string(KV)
    
        sm = ScreenManager()
        sm.add_widget(Demo1(name="demo1"))
        sm.add_widget(Demo2(name="demo2"))

        return sm

    def on_start(self):
        Window.size = [400, 700]

    def send(self):
        text_input = self.root.current_screen.ids.text_input.text
        if text_input != "":
            if len(text_input) < 6:
                size_hint_x = 0.18
            elif len(text_input) < 11:
                size_hint_x = .3
            elif len(text_input) < 16:
                size_hint_x = .4
            elif len(text_input) < 21:
                size_hint_x = .5
            elif len(text_input) < 26:
                size_hint_x = .65
            else:
                size_hint_x = .75

            message = MyMessage(
                text=text_input,
                size_hint_x=size_hint_x,
                halign="right",
                padding=(10, 10)
            )

        user_message = self.root.current_screen.ids.text_input.text
        user_id = self.root.current_screen.ids.AppBarUserId.text
        save_request = requests.post("http://192.168.1.4:8000/send_message", json={"user_id": int(user_id), "message": user_message})

        if save_request.status_code == 200:
            self.root.current_screen.ids.chat_list.add_widget(message)
            self.root.current_screen.ids.text_input.text = ""
            print("Заебись")


if __name__ == "__main__":
    MainApp().run()
