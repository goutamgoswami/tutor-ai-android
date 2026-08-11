```python
import os
import threading
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

from google import genai
from google.genai import types


class TutorApp(App):

    def build(self):
        self.title = "Alumni Tutor AI"

        self.client = None
        self.chat = None

        # Colors
        self.bg_color = get_color_from_hex("#F4F6F9")
        self.primary_color = get_color_from_hex("#3B82F6")
        self.text_dark = get_color_from_hex("#1E293B")

        # Main layout
        self.main_layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=12
        )

        self.main_layout.background_color = self.bg_color

        self.initialize_ai_system()
        self.setup_ui()

        return self.main_layout

    def initialize_ai_system(self):
        """
        Initialize Gemini client.

        Priority:
        1. GEMINI_API_KEY environment variable
        2. .gemini_key file in the application's home directory
        """

        api_key = os.environ.get("GEMINI_API_KEY")

        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                return
            except Exception as e:
                print(f"Gemini initialization error: {e}")

        try:
            config_file = Path.home() / ".gemini_key"

            if config_file.exists():
                api_key = config_file.read_text(
                    encoding="utf-8"
                ).strip()

                if api_key:
                    self.client = genai.Client(
                        api_key=api_key
                    )

        except Exception as e:
            print(f"Could not read Gemini key: {e}")

    def setup_ui(self):

        # Header
        header = BoxLayout(
            orientation="vertical",
            size_hint_y=0.15,
            padding=4
        )

        title_label = Label(
            text="REAL-WORLD ALUMNI TUTOR AI",
            font_size="18sp",
            bold=True,
            color=(1, 1, 1, 1)
        )

        subtitle_label = Label(
            text="Powered by Gemini • Clear Analogy Explorer",
            font_size="11sp",
            color=get_color_from_hex("#E0F2FE")
        )

        header.add_widget(title_label)
        header.add_widget(subtitle_label)

        self.main_layout.add_widget(header)

        # Chat area
        self.scroll_view = ScrollView(
            size_hint_y=0.70
        )

        self.chat_display = Label(
            text=(
                "System > Tutor session started.\n"
                "Please configure your Gemini API key.\n\n"
            ),
            font_size="14sp",
            color=self.text_dark,
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        self.chat_display.bind(
            texture_size=self.chat_display.setter("size")
        )

        self.scroll_view.add_widget(
            self.chat_display
        )

        self.main_layout.add_widget(
            self.scroll_view
        )

        # Input area
        input_frame = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.15,
            spacing=8
        )

        self.input_field = TextInput(
            hint_text="Ask a school topic...",
            multiline=False,
            font_size="15sp",
            size_hint_x=0.75
        )

        self.input_field.bind(
            on_text_validate=self.on_enter_pressed
        )

        self.send_button = Button(
            text="Ask",
            font_size="15sp",
            bold=True,
            background_color=self.primary_color,
            size_hint_x=0.25
        )

        self.send_button.bind(
            on_press=self.on_send_pressed
        )

        input_frame.add_widget(
            self.input_field
        )

        input_frame.add_widget(
            self.send_button
        )

        self.main_layout.add_widget(
            input_frame
        )

        Clock.schedule_once(
            lambda dt: self.start_chat_session(),
            0.5
        )

    def on_enter_pressed(self, instance):
        self.send_message()

    def on_send_pressed(self, instance):
        self.send_message()

    def start_chat_session(self):

        if not self.client:

            self.update_chat_ui(
                "System Warning > Gemini API key was not found."
            )

            return

        system_prompt = (
            "You are an encouraging, expert high school study tutor. "
            "Explain complex topics simply using clear real-world "
            "analogies. Use simple language and examples suitable "
            "for students."
        )

        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7
        )

        try:

            self.chat = self.client.chats.create(
                model="gemini-2.5-flash",
                config=config
            )

            self.update_chat_ui(
                "System > AI tutor is ready. Ask your question."
            )

        except Exception as e:

            self.update_chat_ui(
                f"API Error > Initialization failure: {e}"
            )

    def update_chat_ui(self, message):

        self.chat_display.text += (
            f"{message}\n\n"
        )

        Clock.schedule_once(
            lambda dt: self.scroll_to_bottom(),
            0
        )

    def scroll_to_bottom(self):

        self.scroll_view.scroll_y = 0

    def send_message(self):

        student_text = (
            self.input_field.text.strip()
        )

        if not student_text:
            return

        if not self.chat:

            self.update_chat_ui(
                "System > AI tutor is not ready yet."
            )

            return

        self.update_chat_ui(
            f"Student > {student_text}"
        )

        self.input_field.text = ""

        self.send_button.disabled = True

        threading.Thread(
            target=self.fetch_ai_response,
            args=(student_text,),
            daemon=True
        ).start()

    def fetch_ai_response(self, text_to_send):

        try:

            response = self.chat.send_message(
                text_to_send
            )

            reply_text = response.text

            Clock.schedule_once(
                lambda dt: self.ui_success_callback(
                    reply_text
                )
            )

        except Exception as e:

            error_message = str(e)

            Clock.schedule_once(
                lambda dt: self.ui_error_callback(
                    error_message
                )
            )

    def ui_success_callback(self, reply_text):

        self.update_chat_ui(
            f"Tutor > {reply_text}"
        )

        self.send_button.disabled = False

    def ui_error_callback(self, error_msg):

        self.update_chat_ui(
            f"Error > Connection broken:\n{error_msg}"
        )

        self.send_button.disabled = False


if __name__ == "__main__":
    TutorApp().run()
```
