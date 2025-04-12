import subprocess
import datetime
import webbrowser
import os
import cv2
import numpy as np
import time
import requests
import json
import getpass
from pathlib import Path
from bs4 import BeautifulSoup
import speech_recognition as sr
import subprocess
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import smtplib
import ctypes
import time
import requests
import json
import getpass
import wmi
from pathlib import Path
from bs4 import BeautifulSoup
import speech_recognition as sr
from urllib.request import urlopen
import wolframalpha
import pyautogui
import csv
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pywinauto import application
import wolframalpha
import pyautogui
import csv
import pandas as pd
import random
import pyttsx3
from gtts import gTTS
import tempfile
import platform
from ultralytics import YOLO
import pyttsx3
from ambulance_service import book_ambulance, notify_nearby_hospitals, open_tracking_interface
from location_service import get_precise_location
from language_manager import LanguageManager

# Initialize systems
lang_manager = LanguageManager()
recognizer = sr.Recognizer()

# Define directories and file formats
DIRECTORIES = {
    "HTML": [".html", ".htm", ".xhtml"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".svg"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mkv"],
    "DOCUMENTS": [".docx", ".doc", ".pdf", ".xls", ".xlsx", ".pptx"],
    "ARCHIVES": [".zip", ".rar", ".tar", ".gz"],
    "AUDIO": [".mp3", ".wav", ".aac"],
    "PLAINTEXT": [".txt"],
    "PYTHON": [".py"],
    "XML": [".xml"],
    "EXE": [".exe"],
    "SHELL": [".sh"]
}
FILE_FORMATS = {file_format: directory for directory, file_formats in DIRECTORIES.items() for file_format in file_formats}



def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        print("Good Morning ")
        speak("Good Morning ")
        
    elif 12 <= hour < 18:
        print("Good Afternoon ")
        speak("Good Afternoon ")
    else:
        print("Good Evening ")
        speak("Good Evening ")
    
    print("I am your Assistant, divya")
    speak("I am your Assistant, divya")
    


def organizeFiles():
    for entry in os.scandir():
        if entry.is_file():
            file_path = Path(entry.name)
            file_format = file_path.suffix.lower()
            if file_format in FILE_FORMATS:
                directory_path = Path(FILE_FORMATS[file_format])
                directory_path.mkdir(exist_ok=True)
                file_path.rename(directory_path.joinpath(file_path))
    
    try:
        os.mkdir("OTHER")
    except FileExistsError:
        pass

    for entry in os.scandir():
        try:
            if entry.is_dir():
                os.rmdir(entry)
            else:
                os.rename(entry.path, Path("OTHER") / Path(entry.name))
        except Exception as e:
            print(f"Error organizing file {entry.name}: {e}")


def send_whatsapp_message(phone_number, message):
    try:
        # Open WhatsApp Web
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        webbrowser.open(whatsapp_url)

        # Wait for WhatsApp Web to load and for user to scan QR code
        print("Please scan the QR code to log in.")
        time.sleep(20)  # Increase if needed

        # Use pywinauto to focus on the browser window
        app = application.Application().connect(title_re=".*WhatsApp.*")
        app_window = app.window(title_re=".*WhatsApp.*")
        app_window.set_focus()

        # Simulate pressing 'Enter' to send the message
        time.sleep(2)  # Wait for the message box to be focused
        pyautogui.press('enter')

        print(f"Message sent successfully to {phone_number}!")

    except Exception as e:
        print(f"Failed to send message: {str(e)}")

# Example usage
def trigger_alert():
    recipient_number = '918555874504'  # The recipient's phone number in international format without "+"
    alert_message = "emergency"  # The alert message

    send_whatsapp_message(recipient_number, alert_message)


def playMusic():
    print("which song you want to search")
    speak("which song you want to search")
    search = takeCommand()
    url = f"https://www.youtube.com/search?q={search}"
    webbrowser.open(url)
    time.sleep(5)  # Wait for YouTube to load
    pyautogui.press('enter')
    pyautogui.press('enter')

def pauseMusic():
    """ Pause the currently playing music """
    print("Pausing music")
    speak("Pausing music")
    pyautogui.press('space')  # Press space to pause

def resumeMusic():
    """ Resume the currently playing music """
    speak("Resuming music")
    pyautogui.press('space')  # Press space to resume

def stopMusic():
    """ Stop the music and close YouTube """
    speak("Stopping the music and closing YouTube")
    pyautogui.hotkey('ctrl', 'w')  # Close the current tab
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'w')  # Close the tab if it is still open


def get_current_time():
    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    print(f"Current time is {current_hour:02d}:{current_minute:02d}")
    return current_hour, current_minute

def set_alarm(alarm_hour, alarm_minute, medication_name):
    while True:
        current_hour, current_minute = get_current_time()

        # Check if current time matches the alarm time
        if current_hour == alarm_hour and current_minute == alarm_minute:
            print("Reminder take "+ medication_name)
            speak("Reminder take "+ medication_name)
            break
        # Wait for 1 minute before checking the time again
        time.sleep(60)

# List of general jokes
general_jokes = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call fake spaghetti? An impasta!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "I'm reading a book about anti-gravity. It's impossible to put down.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, I am having trouble connecting to the service.")
        return ""

def tell_joke():
    import random
    # Select a random general joke from the list
    joke = random.choice(general_jokes)
    speak(joke)
    print(joke)

def main():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if 'joke' in command:
            tell_joke()
        elif 'one more' in command:
            tell_joke()
        
        elif 'exit' in command:
            speak("Goodbye!")
            break


# Load the CSV file
data = pd.read_csv('d.csv')

# Preprocess data to create a lookup table for diseases
disease_dict = {}
for i, row in data.iterrows():
    disease = row['disease'].lower()
    symptoms = row['symptoms'].lower()
    food_items = row['food_items']
    nutritional_values = row['nutritional_values']
    health_benefits = row['health_benefits']
    disease_dict[disease] = {
        'food_items': food_items,
        'nutritional_values': nutritional_values,
        'health_benefits': health_benefits,
        'symptoms': symptoms
    }

# Function to recognize speech input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say the disease or symptoms:")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            engine.say("Sorry, I did not understand that.")
            engine.runAndWait()
            return None

# Function to find the diet plan based on input
def find_diet_plan(input_text):
    for disease, info in disease_dict.items():
        if disease in input_text or any(symptom in input_text for symptom in info['symptoms'].split(',')):
            return info
    return None

# Main function to run the voice assistant
def voice_assistant():
    while True:
        user_input = recognize_speech()
        if user_input:
            diet_plan = find_diet_plan(user_input)
            if diet_plan:
                response = f"For {user_input}, consider consuming {diet_plan['food_items']}. These foods are beneficial because {diet_plan['health_benefits']}."
                print(response)
                engine.say(response)
                engine.runAndWait()
            elif user_input == 'exit' :
                break
                
            else:
                engine.say("Sorry, I couldn't find a specific diet plan for your symptoms. Please consult a doctor for a personalized diet.")
                engine.runSAndWait()
            


def fetch_medicine_info(medicine_name):
    with open('c.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['medicine_name'].lower() == medicine_name.lower():
                description = row['description']
                uses = row['uses']
                dosage = row['dosage']
                return description, uses, dosage
    return None, None, None

def get_audio_player():
    """Determine the best audio player for the system"""
    system = platform.system()
    if system == "Windows":
        return 'start'
    elif system == "Darwin":  # macOS
        return 'afplay'
    else:  # Linux
        if subprocess.run(['which', 'mpg123'], capture_output=True).returncode == 0:
            return 'mpg123'
        elif subprocess.run(['which', 'play'], capture_output=True).returncode == 0:
            return 'play'
        else:
            return 'aplay'

AUDIO_PLAYER = get_audio_player()

def speak(text, wait=True):
    """
    Improved text-to-speech function with multiple fallback options
    and proper language support
    """
    lang_code = lang_manager.current_lang
    print(f"SYSTEM: {text}")  # Always print to console

    try:
        # First try gTTS for Indian languages
        if lang_code in ['ta', 'hi', 'te', 'kn', 'ml', 'bn', 'mr']:
            try:
                tts = gTTS(text=text, lang=lang_code)
                with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
                    temp_path = f"{fp.name}.mp3"  # Workaround for Windows
                    tts.save(temp_path)
                    
                    # Play the audio file
                    if AUDIO_PLAYER == 'start':  # Windows
                        os.startfile(temp_path)
                    elif AUDIO_PLAYER == 'afplay':  # macOS
                        subprocess.run(['afplay', temp_path])
                    else:  # Linux
                        subprocess.run([AUDIO_PLAYER, temp_path])
                    
                    # Wait for playback to complete if requested
                    if wait:
                        time.sleep(len(text.split()) * 0.5)  # Approximate duration
                    return
            except Exception as gtts_error:
                print(f"gTTS failed: {gtts_error}")
                # Fall through to pyttsx3

        # Fallback to pyttsx3
        try:
            engine = pyttsx3.init()
            
            # Configure voice properties
            engine.setProperty('rate', 150)  # Slower speech
            engine.setProperty('volume', 1.0)
            
            # Try to set appropriate voice for the language
            voices = engine.getProperty('voices')
            voice_map = {
                'hi': 'hi-IN',
                'ta': 'ta-IN',
                'te': 'te-IN',
                'kn': 'kn-IN',
                'ml': 'ml-IN',
                'bn': 'bn-IN',
                'mr': 'mr-IN'
            }
            
            if lang_code in voice_map:
                for voice in voices:
                    if voice_map[lang_code] in voice.id:
                        engine.setProperty('voice', voice.id)
                        break
            
            engine.say(text)
            engine.runAndWait()
            return
        except Exception as pyttsx_error:
            print(f"pyttsx3 failed: {pyttsx_error}")
            # Fall through to system commands

        # Ultimate fallback using system commands
        if platform.system() == "Darwin":  # macOS
            subprocess.run(['say', text])
        elif platform.system() == "Linux":
            subprocess.run(['spd-say', text])
        
    except Exception as e:
        print(f"All TTS methods failed: {e}")
        # Last resort - just print to console
        print(f"(Voice output failed) SYSTEM: {text}")

def takeCommand():
    """Improved speech recognition with better error handling"""
    lang_codes = {
        'en': 'en-IN',
        'hi': 'hi-IN',
        'ta': 'ta-IN',
        'te': 'te-IN',
        'kn': 'kn-IN',
        'ml': 'ml-IN',
        'bn': 'bn-IN',
        'mr': 'mr-IN'
    }
    
    with sr.Microphone() as source:
        print(lang_manager.get_text("system", "listening"))
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("Listening timed out")
            return ""
    
    try:
        query = recognizer.recognize_google(audio, language=lang_codes.get(lang_manager.current_lang, 'en-IN'))
        print(f"USER: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Recognition error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    speak(lang_manager.get_text("system", "not_understood"))
    return ""

def handleEmergency():
    """Improved emergency handling with better feedback"""
    speak(lang_manager.get_text("ambulance", "emergency_triggered"))
    
    try:
        loc, address = get_precise_location()
        if not loc:
            raise ValueError("Location error")
            
        speak(f"{lang_manager.get_text('ambulance', 'location_found')} {address.split(',')[0]}")
        
        booking = book_ambulance(*loc, lang_manager.current_lang)
        if booking['success']:
            speak(f"{lang_manager.get_text('ambulance', 'ambulance_coming')} {booking['eta']}")
            hospitals = notify_nearby_hospitals(*loc, lang_manager.current_lang)
            speak(f"{lang_manager.get_text('ambulance', 'nearest_hospital')} {hospitals[0]['name']}")
            open_tracking_interface(booking['tracking_url'])
        else:
            speak(lang_manager.get_text("ambulance", "booking_failed"))
    except Exception as e:
        print(f"Emergency error: {e}")
        speak(lang_manager.get_text("ambulance", "manual_call"))

def detection():
    class FallDetector:
        def __init__(self):
            # Initialize background subtractor
            self.fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)
            
            # Fall detection parameters
            self.aspect_ratio_threshold = 0.6  # Lowered for better sensitivity
            self.min_contour_area = 2000       # Increased to ignore small movements
            self.stationary_time = 1.5         # Seconds of inactivity to confirm fall
            self.impact_threshold = 2.0        # Size change ratio for impact detection
            
            # State variables
            self.last_motion_time = time.time()
            self.last_aspect_ratio = None
            self.fall_detected = False
            self.alert_cooldown = 0

        def detect_fall(self, frame):
            # Preprocessing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (7, 7), 0)
            
            # Background subtraction
            fgmask = self.fgbg.apply(blurred)
            _, fgmask = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY)
            
            # Noise removal
            kernel = np.ones((7,7), np.uint8)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            motion_detected = False
            fall_conditions_met = False
            current_aspect_ratio = None
            
            for contour in contours:
                if cv2.contourArea(contour) < self.min_contour_area:
                    continue
                    
                motion_detected = True
                self.last_motion_time = time.time()
                
                # Get bounding box
                x, y, w, h = cv2.boundingRect(contour)
                current_aspect_ratio = float(h)/w
                
                # Check for sudden change in aspect ratio (impact)
                if self.last_aspect_ratio and (self.last_aspect_ratio / current_aspect_ratio) > self.impact_threshold:
                    print(f"Impact detected! Ratio change: {self.last_aspect_ratio:.2f} -> {current_aspect_ratio:.2f}")
                    fall_conditions_met = True
                
                # Check if person is lying down
                if current_aspect_ratio < self.aspect_ratio_threshold:
                    fall_conditions_met = True
                
                self.last_aspect_ratio = current_aspect_ratio
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                cv2.putText(frame, f"Ratio: {current_aspect_ratio:.2f}", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            
            # Fall confirmation logic
            if fall_conditions_met:
                inactivity_duration = time.time() - self.last_motion_time
                print(f"Fall conditions met. Inactivity: {inactivity_duration:.2f}s")
                
                if inactivity_duration > self.stationary_time:
                    if not self.fall_detected:
                        self.fall_detected = True
                        return True, frame
            else:
                self.fall_detected = False
            
            return False, frame

    def process_video_file(video_path):
        detector = FallDetector()
        
        if not os.path.exists(video_path):
            print(f"Error: File not found at {video_path}")
            return
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000/fps) if fps > 0 else 30
        
        print("Processing video...")
        print("Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame = cv2.resize(frame, (640, 480))  # Standardize size
            
            fall_detected, processed_frame = detector.detect_fall(frame)
            
            if fall_detected:
                cv2.putText(processed_frame, "FALL DETECTED!", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print("ALERT: Fall detected!")
            
            cv2.imshow('Fall Detection', processed_frame)
            
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        print("Processing complete")

    if __name__ == "__main__":
        video_file = "fall.mp4"  # Change to your video filename
        
        # List files in current directory to help debugging
        print("Files in current directory:")
        print(os.listdir('.'))
        
        process_video_file(video_file)
def object():
    # Initialize Text-to-Speech engine
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    # Load YOLOv8x model (most accurate)
    model = YOLO("yolov8x.pt")

    # Start webcam
    cap = cv2.VideoCapture(0)

    # Set resolution (HD)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    spoken_objects = set()
    last_spoken_time = time.time()
    speak_interval = 5  # seconds
    confidence_threshold = 0.4  # Only consider predictions above this confidence

    print("🎥 AI Assistant is running with YOLOv8x... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection
        results = model(frame)[0]

        # Store currently detected object labels
        current_objects = []
        for box in results.boxes:
            if box.conf[0] < confidence_threshold:
                continue
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            current_objects.append(label)

        # Annotate and display the frame
        annotated_frame = results.plot()
        cv2.imshow("AI Assistant - Object Detection", annotated_frame)

        # Speak new objects or at intervals
        current_time = time.time()
        if current_objects:
            unique_objects = set(current_objects)
            new_objects = unique_objects - spoken_objects
            if new_objects or (current_time - last_spoken_time) > speak_interval:
                text = "I see: " + ", ".join(unique_objects)
                print("🔊 " + text)
                engine.say(text)
                engine.runAndWait()
                spoken_objects = unique_objects
                last_spoken_time = current_time

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
def change_language():
    """Improved language selection with better feedback"""
    speak("Available languages:")
    for code, name in lang_manager.languages.items():
        speak(name, wait=False)
        time.sleep(0.5)  # Pause between language announcements
    
    for attempt in range(3):
        speak("Please say the name of your preferred language")
        lang_code = takeCommand()
        if not lang_code:
            continue
            
        # Check for both language names and codes
        matched_code = None
        for code, name in lang_manager.languages.items():
            if name.lower() in lang_code.lower() or code.lower() in lang_code.lower():
                matched_code = code
                break
                
        if matched_code and lang_manager.set_language(matched_code):
            speak(f"Language changed to {lang_manager.languages[matched_code]}")
            return
            
    speak("Could not change language. Please try again later.")

def main():
    """Main program with improved initialization and error handling"""
    # Initial system test
    try:
        speak("Initializing voice assistant system", wait=True)
    except Exception as e:
        print(f"Initialization warning: {e}")

    # Language selection
    supported_langs = ", ".join(lang_manager.languages.values())
    speak(f"Please say your preferred language. Supported languages are: {supported_langs}")
    
    for attempt in range(3):
        user_lang = takeCommand()
        if not user_lang:
            if attempt < 2:
                speak("I didn't hear anything. Please try again.")
            continue
            
        # Check for both language names and codes
        matched_code = None
        for code, name in lang_manager.languages.items():
            if name.lower() in user_lang.lower() or code.lower() in user_lang.lower():
                matched_code = code
                break
                
        if matched_code:
            if lang_manager.set_language(matched_code):
                speak(f"Language set to {lang_manager.languages[matched_code]}")
                break
            else:
                speak("Sorry, that language isn't available")
        else:
            speak("I didn't understand. Please say the language name again.")
    
    else:
        speak("Defaulting to English")
        lang_manager.set_language('en')

    # Main command loop
    speak(lang_manager.get_text("system", "welcome"))
    
    while True:
        query = takeCommand()

        if "hello" in query:
            print("Hello, how are you ?")
            speak("Hello, how are you ?")
        elif "i am fine" in query:
            print("that's great,")
            speak("that's great,")
        elif "how are you" in query:
            print("I am doing great")
            speak("I am doing great")
        elif "thank you" in query:
            print("you are welcome,")
            speak("you are welcome,")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Sir, the time is {strTime}")
            speak(f"Sir, the time is {strTime}")
        elif "object" in query:
            object()
        elif 'medicine' in query or 'tablet' in query:
            print("Please tell me the name of the medicine.")
            speak("Please tell me the name of the medicine.")
            medicine_name = takeCommand()

            if medicine_name != "None":
                description, uses, dosage = fetch_medicine_info(medicine_name)
                
                if description and uses and dosage:
                    print("Here is the information I found.")
                    speak("Here is the information I found.")
                    print(f"Description: {description}")
                    speak(f"Description: {description}")
                    print(f"Uses: {uses}")
                    speak(f"Uses: {uses}")
                    print(f"Dosage: {dosage}")
                    speak(f"Dosage: {dosage}")
                    print('thanks for your time')
                    speak('thanks for your time')
                else:
                    speak("Sorry, I couldn't find information on that medicine.")
        elif 'alert' in query:
            print("Sure,I will send an alert as soon as possible.")
            speak("Sure,I will send an alert as soon as possible.")
            trigger_alert()

        
        elif "set alarm" in query:
            speak("set the alarm hour in 24-hour format.")
            alarm_hour = takeCommand()
            if alarm_hour:
                alarm_hour = int(alarm_hour)
            speak("Please set the alarm minute.")
            alarm_minute = takeCommand()
            if alarm_minute:
                alarm_minute = int(alarm_minute)
            
            if alarm_hour is not None and alarm_minute is not None:
                print("medication_name")
                speak("medication_name")
                medication_name = takeCommand()
                print(f"Alarm is set for {alarm_hour:02d}:{alarm_minute:02d}.")
                speak(f"Alarm is set for {alarm_hour:02d}:{alarm_minute:02d}.")
                set_alarm(alarm_hour, alarm_minute, medication_name)

        elif 'tell me a joke' in query:
            main()

        elif "play music" in query:
            playMusic()

        elif "pause" in query:
            pauseMusic()

        elif "play" in query:
            resumeMusic()

        elif "resume" in query:
            stopMusic()
        elif "diet plan" in query :
            voice_assistant()

        elif "weather" in query:
            speak("give a comand to search")
            search = takeCommand()
            url = f"https://www.google.com/search?q={search}"
            r  = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div", class_ = "BNeawe").text
            speak(f"current{search} is {temp}")

        elif "detection" in query:
            detection()
        elif 'emergency' in query or 'ambulance' in query or 'அவசரம்' in query:
            handleEmergency()
            print("Sure,I will send an alert as soon as possible.")
            speak("Sure,I will send an alert as soon as possible.")
            trigger_alert()
        elif 'change language' in query or 'भाषा बदलें' in query or 'மொழி மாற்று' in query:
            change_language()
        elif 'exit' in query or 'stop' in query or 'बंद करो' in query or 'நிறுத்து' in query:
            speak(lang_manager.get_text("system", "exit"))
            break
        else:
            speak(lang_manager.get_text("system", "not_understood"))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Fatal error: {e}")
        speak("A system error occurred. The program will now exit.")