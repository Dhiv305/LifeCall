import webbrowser
import random
from language_manager import LanguageManager

lang_manager = LanguageManager()

def book_ambulance(lat, lng, lang='en'):
    lang_manager.set_language(lang)
    hospitals = [
        {"name": lang_manager.get_text("system", "city_hospital"), "distance": "2.5 km", "contact": "108"},
        {"name": lang_manager.get_text("system", "metro_medical"), "distance": "3.1 km", "contact": "102"}
    ]
    
    return {
        "success": True,
        "message": lang_manager.get_text("ambulance", "booking_success"),
        "ambulance_id": f"AMB{random.randint(1000,9999)}",
        "eta": f"{random.randint(5, 15)} {lang_manager.get_text('system', 'minutes')}",
        "driver_name": f"{lang_manager.get_text('system', 'driver')} {random.choice(['John', 'Priya'])}",
        "tracking_url": f"https://maps.google.com/?q={lat},{lng}"
    }

def notify_nearby_hospitals(lat, lng, lang='en'):
    lang_manager.set_language(lang)
    return [
        {
            "name": lang_manager.get_text("system", "city_hospital"),
            "contact": "108",
            "specialties": [lang_manager.get_text("medical", "emergency")]
        },
        {
            "name": lang_manager.get_text("system", "metro_trauma"),
            "contact": "102",
            "specialties": [lang_manager.get_text("medical", "accident")]
        }
    ]

def open_tracking_interface(url):
    webbrowser.open(url)
    print(lang_manager.get_text("ambulance", "tracking_started"))