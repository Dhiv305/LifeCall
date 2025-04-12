import json
from pathlib import Path

class LanguageManager:
    def __init__(self):
        self.languages = {
            'en': 'English',
            'hi': 'Hindi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'bn': 'Bengali',
            'mr': 'Marathi'
        }
        self.translations = {}
        self.current_lang = 'en'
        self.load_translations()
        
    def load_translations(self):
        lang_dir = Path('lang')
        lang_dir.mkdir(exist_ok=True)
        
        for lang_code in self.languages:
            try:
                with open(lang_dir/f'{lang_code}.json', 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
            except FileNotFoundError:
                self.translations[lang_code] = self.create_template(lang_code)
                with open(lang_dir/f'{lang_code}.json', 'w', encoding='utf-8') as f:
                    json.dump(self.translations[lang_code], f, ensure_ascii=False, indent=2)

    def create_template(self, lang_code):
        return {
            "system": {
                "welcome": f"Welcome in {self.languages[lang_code]}",
                "good_morning": "Good morning",
                "good_afternoon": "Good afternoon",
                "good_evening": "Good evening",
                "assistant_name": "I am your Assistant",
                "listening": "Listening...",
                "not_understood": "Sorry, I didn't understand",
                "command_prompt": "How can I help?",
                "exit": "Goodbye!",
                "thank_you": "Thank you",
                "driver": "Driver"
            },
            "ambulance": {
                "emergency_triggered": "Emergency detected! Stay calm.",
                "location_found": "Located at",
                "booking_success": "Ambulance booked",
                "ambulance_coming": "Ambulance coming in",
                "driver_contact": "Driver will contact",
                "nearest_hospital": "Nearest hospital",
                "manual_call": "Please call emergency number",
                "tracking_started": "Tracking ambulance"
            }
        }

    def set_language(self, lang_code):
        if lang_code in self.languages:
            self.current_lang = lang_code
            return True
        return False

    def get_text(self, category, key):
        try:
            return self.translations[self.current_lang][category][key]
        except KeyError:
            return self.translations['en'][category][key]