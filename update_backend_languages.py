from pathlib import Path

path = Path("backend/api.py")
source = path.read_text(encoding="utf-8")

marker = "\n}\n\ndef translate_text(text, language):"
if source.count(marker) != 1:
    raise SystemExit("STOP: Expected language dictionary boundary not found. No changes made.")

new_languages = '''
    "mr": {
        "name": "मराठी",
        "voice": "mr-IN-AarohiNeural",
        "labels": {
            "plant": "वनस्पती", "disease": "रोग",
            "confidence": "विश्वास पातळी", "accuracy": "चाचणी अचूकता",
            "level": "विश्वास पातळी", "causes": "रोगाची कारणे",
            "medicine": "औषध / उपचार", "prevention": "प्रतिबंध",
            "high": "उच्च विश्वास", "moderate": "मध्यम विश्वास",
            "low": "कमी विश्वास", "speak": "निकाल ऐका",
            "stop": "आवाज थांबवा", "loading": "प्रतिमेचे विश्लेषण सुरू आहे...",
            "error": "त्रुटी",
        },
    },
    "te": {
        "name": "తెలుగు",
        "voice": "te-IN-ShrutiNeural",
        "labels": {
            "plant": "మొక్క", "disease": "వ్యాధి",
            "confidence": "నమ్మక స్థాయి", "accuracy": "పరీక్ష ఖచ్చితత్వం",
            "level": "నమ్మక స్థాయి", "causes": "వ్యాధి కారణాలు",
            "medicine": "మందు / చికిత్స", "prevention": "నివారణ",
            "high": "అధిక నమ్మకం", "moderate": "మధ్యస్థ నమ్మకం",
            "low": "తక్కువ నమ్మకం", "speak": "ఫలితాన్ని వినండి",
            "stop": "వాయిస్ ఆపండి", "loading": "చిత్రాన్ని విశ్లేషిస్తోంది...",
            "error": "లోపం",
        },
    },
    "ta": {
        "name": "தமிழ்",
        "voice": "ta-IN-PallaviNeural",
        "labels": {
            "plant": "தாவரம்", "disease": "நோய்",
            "confidence": "நம்பிக்கை நிலை", "accuracy": "சோதனை துல்லியம்",
            "level": "நம்பிக்கை நிலை", "causes": "நோய்க்கான காரணங்கள்",
            "medicine": "மருந்து / சிகிச்சை", "prevention": "தடுப்பு",
            "high": "அதிக நம்பிக்கை", "moderate": "மிதமான நம்பிக்கை",
            "low": "குறைந்த நம்பிக்கை", "speak": "முடிவைக் கேளுங்கள்",
            "stop": "குரலை நிறுத்து", "loading": "படத்தை ஆய்வு செய்கிறது...",
            "error": "பிழை",
        },
    },'''

source = source.replace(marker, "\n" + new_languages + marker, 1)

old_target = 'target = {"hi": "hi", "kn": "kn"}.get(language)'
new_target = 'target = {"hi": "hi", "kn": "kn", "mr": "mr", "te": "te", "ta": "ta"}.get(language)'

if source.count(old_target) != 1:
    raise SystemExit("STOP: Translation target mapping not found exactly once.")

source = source.replace(old_target, new_target, 1)
path.write_text(source, encoding="utf-8")
print("Updated backend language dictionary and translation targets.")
