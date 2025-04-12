from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
import threading
import datetime
import webbrowser
import os
import time
import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import tempfile
import platform
import pygame
from pygame import mixer
from language_manager import LanguageManager
from ambulance_service import book_ambulance, notify_nearby_hospitals, open_tracking_interface
from location_service import get_precise_location

# Initialize systems
lang_manager = LanguageManager()
recognizer = sr.Recognizer()

# Kivy GUI Layout
Builder.load_string('''
<VoiceAssistantGUI>:
    orientation: 'vertical'
    padding: 10
    spacing: 10
    
    BoxLayout:
        size_hint_y: None
        height: 40
        Label:
            text: 'Voice Assistant'
            font_size: 24
            bold: True
    
    ScrollView:
        size_hint: (1, 0.7)
        TextInput:
            id: output_text
            text: 'Assistant ready...\\n'
            readonly: True
            font_size: 18
            size_hint_y: None
            height: max(self.minimum_height, self.parent.height)
    
    BoxLayout:
        size_hint_y: None
        height: 40
        Button:
            text: 'Speak'
            on_press: root.start_listening()
        Button:
            text: 'Emergency'
            background_color: (1, 0, 0, 1)
            on_press: root.handle_emergency()
    
    BoxLayout:
        size_hint_y: None
        height: 40
        Button:
            text: 'Change Language'
            on_press: root.change_language()
        Button:
            text: 'Exit'
            on_press: app.stop()
''')

class VoiceAssistantGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = None
        self.init_audio()
        self.command_history = []
        
    def init_audio(self):
        try:
            pygame.init()
            mixer.init()
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
        except Exception as e:
            self.log_message(f"Audio init error: {str(e)}")

    def log_message(self, message):
        self.ids.output_text.text += f"{message}\n"
        print(message)

    def speak(self, text):
        def _speak():
            try:
                if platform.system() == "Windows":
                    self.engine.say(text)
                    self.engine.runAndWait()
                else:
                    tts = gTTS(text=text, lang=lang_manager.current_lang)
                    audio_bytes = io.BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    mixer.music.load(audio_bytes)
                    mixer.music.play()
                    while mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
            except Exception as e:
                self.log_message(f"Speech error: {str(e)}")
        
        threading.Thread(target=_speak).start()

    def start_listening(self):
        self.log_message("Listening...")
        threading.Thread(target=self.take_command).start()

    def take_command(self):
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                query = recognizer.recognize_google(audio)
                self.log_message(f"You said: {query}")
                self.process_command(query.lower())
        except Exception as e:
            self.log_message(f"Listening error: {str(e)}")

    def process_command(self, query):
        # Add your existing command processing logic here
        if "hello" in query:
            response = "Hello, how are you?"
        elif "time" in query:
            response = datetime.datetime.now().strftime("%H:%M:%S")
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            response = "Opening YouTube"
        # Add all other command conditions from your main()
        else:
            response = "I didn't understand that command"
        
        self.speak(response)
        self.log_message(f"Assistant: {response}")

    def handle_emergency(self):
        def _emergency():
            try:
                self.speak("Emergency mode activated!")
                loc, address = get_precise_location()
                if loc:
                    self.speak(f"Location found: {address.split(',')[0]}")
                    booking = book_ambulance(*loc, lang_manager.current_lang)
                    if booking['success']:
                        self.speak(f"Ambulance coming in {booking['eta']}")
            except Exception as e:
                self.speak("Emergency call failed")
                self.log_message(f"Emergency error: {str(e)}")
        
        threading.Thread(target=_emergency).start()

    def change_language(self):
        def _change_language():
            self.speak("Available languages:")
            for code, name in lang_manager.languages.items():
                self.speak(name)
                time.sleep(0.3)
            
            self.speak("Please say your preferred language")
            lang_code = self.take_command()
            if lang_code:
                for code, name in lang_manager.languages.items():
                    if name.lower() in lang_code.lower() or code.lower() in lang_code.lower():
                        lang_manager.set_language(code)
                        self.speak(f"Language changed to {name}")
                        return
        
        threading.Thread(target=_change_language).start()

class VoiceAssistantApp(App):
    def build(self):
        Window.size = (400, 600)
        return VoiceAssistantGUI()

if __name__ == '__main__':
    VoiceAssistantApp().run()