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
        
        # Original Palette Constants
        self.bg_color = get_color_from_hex("#F4F6F9")
        self.primary_color = get_color_from_hex("#3B82F6")
        self.text_dark = get_color_from_hex("#1E293B")
        
        # Main Layout
        self.main_layout = BoxLayout(orientation='vertical', spacing=10, padding=12)
        
        self.initialize_ai_system()
        self.setup_ui()
        return self.main_layout

    def initialize_ai_system(self):
        if "GEMINI_API_KEY" in os.environ:
            self.client = genai.Client()
            return
        config_file = Path.home() / ".gemini_key"
        if config_file.exists():
            try:
                api_key = config_file.read_text().strip()
                if api_key:
                    self.client = genai.Client(api_key=api_key)
                    return
            except Exception:
                pass

    def setup_ui(self):
        # Header Area
        header = BoxLayout(orientation='vertical', size_hint_y=0.15, padding=4)
        title_label = Label(text="🚀 REAL-WORLD ALUMNI TUTOR AI", font_size='18sp', bold=True, color=(1,1,1,1))
        subtitle_label = Label(text="Powered by Gemini • Clear Analogy Explorer", font_size='11sp', color=get_color_from_hex("#E0F2FE"))
        header.add_widget(title_label)
        header.add_widget(subtitle_label)
        self.main_layout.add_widget(header)

        # Scrollable Chat Display Area
        self.scroll_view = ScrollView(size_hint_y=0.7)
        self.chat_display = Label(
            text="System > Tutor session started. Please ensure your GEMINI_API_KEY is configured.\n\n",
            font_size='14sp', color=self.text_dark, size_hint_y=None, halign='left', valign='top'
        )
        self.chat_display.bind(texture_size=self.chat_display.setter('size'))
        self.scroll_view.add_widget(self.chat_display)
        self.main_layout.add_widget(self.scroll_view)

        # Input Row Area Bar
        input_frame = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=8)
        self.input_field = TextInput(hint_text="Ask a school topic...", multiline=False, font_size='15sp', size_hint_x=0.75)
        self.input_field.bind(on_text_validate=lambda instance: self.send_message())
        
        self.send_button = Button(text="Ask", font_size='15sp', bold=True, background_color=self.primary_color, size_hint_x=0.25)
        self.send_button.bind(on_press=lambda instance: self.send_message())
        
        input_frame.add_widget(self.input_field)
        input_frame.add_widget(self.send_button)
        self.main_layout.add_widget(input_frame)
        
        Clock.schedule_once(lambda dt: self.start_chat_session(), 0.5)

    def start_chat_session(self):
        if not self.client:
            self.update_chat_ui("System Warning > Key not found automatically. Make sure your environment has GEMINI_API_KEY set up.")
            try:
                # Basic execution initialization fallback
                self.client = genai.Client()
            except Exception:
                return

        system_prompt = "You are an encouraging, expert high school study tutor. Explain complex topics simply using analogies."
        config = types.GenerateContentConfig(system_instruction=system_prompt, temperature=0.7)
        try:
            self.chat = self.client.chats.create(model="gemini-2.5-flash", config=config)
        except Exception as e:
            self.update_chat_ui(f"API Error > Initialization failure: {e}")

    def update_chat_ui(self, message):
        self.chat_display.text += f"{message}\n\n"
        self.scroll_view.scroll_y = 0

    def send_message(self):
        student_text = self.input_field.text.strip()
        if not student_text or not self.chat: return
        self.update_chat_ui(f"Student > {student_text}")
        self.input_field.text = ""
        self.send_button.disabled = True
        threading.Thread(target=self.fetch_ai_response, args=(student_text,), daemon=True).start()

    def fetch_ai_response(self, text_to_send):
        try:
            response = self.chat.send_message(text_to_send)
            Clock.schedule_once(lambda dt: self.ui_success_callback(response.text))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.ui_error_callback(str(e)))

    def ui_success_callback(self, reply_text):
        self.update_chat_ui(f"Tutor > {reply_text}")
        self.send_button.disabled = False

    def ui_error_callback(self, error_msg):
        self.update_chat_ui(f"Error > Connection broken: {error_msg}")
        self.send_button.disabled = False

if __name__ == '__main__':
    TutorApp().run()
