from pathlib import Path
import re

path = Path("frontend/index.html")
source = path.read_text(encoding="utf-8")
original = source

# 1. Update the language selector.
pattern = r'<select id="language">.*?</select>'
replacement = """<select id="language">
            <option value="en">English</option>
            <option value="kn">ಕನ್ನಡ</option>
            <option value="hi">हिन्दी</option>
            <option value="mr">मराठी</option>
            <option value="te">తెలుగు</option>
            <option value="ta">தமிழ்</option>
        </select>"""

source, count = re.subn(
    pattern, lambda _: replacement, source, count=1, flags=re.S
)
if count != 1:
    raise SystemExit("STOP: Language selector was not found.")

# 2. Add UI dictionaries, inheriting English defaults for any
#    labels that have not yet been translated.
marker = '\n};\n\n\n/* =========================================================\n   CLASS TRANSLATIONS'
if source.count(marker) != 1:
    raise SystemExit("STOP: UI dictionary boundary was not found.")

languages = r'''
    ,
    mr: {
        ...UI.en,
        language: "भाषा",
        pageTitle: "वनस्पती रोग ओळख",
        upload: "पानाचा फोटो अपलोड करा",
        class: "वनस्पतीचा प्रकार निवडा",
        chooseClass: "प्रकार निवडा",
        chooseImage: "नमुना फोटो पाहण्यासाठी प्रकार निवडा.",
        predict: "रोग ओळखा",
        camera: "कॅमेरा वापरा",
        voice: "आवाजाने प्रश्न विचारा",
        voicePlaceholder: "मायक्रोफोन दाबून प्रश्न विचारा...",
        speakQuestion: "प्रश्न बोला",
        stopInput: "आवाज इनपुट थांबवा",
        samples: "पानांचे नमुना फोटो",
        plant: "वनस्पती",
        disease: "रोग",
        confidence: "विश्वास पातळी",
        accuracy: "चाचणी अचूकता",
        level: "विश्वास पातळी",
        causes: "रोगाची कारणे",
        medicine: "औषध / उपचार",
        prevention: "प्रतिबंध",
        speak: "निकाल ऐका",
        stopVoice: "आवाज थांबवा",
        listening: "ऐकत आहे...",
        processing: "प्रक्रिया सुरू आहे...",
        predictionReady: "रोग ओळख पूर्ण झाली.",
        noImage: "कृपया पानाचा फोटो अपलोड करा किंवा निवडा.",
        loading: "लोड होत आहे...",
        noSamples: "नमुना फोटो उपलब्ध नाहीत."
    },
    te: {
        ...UI.en,
        language: "భాష",
        pageTitle: "మొక్కల వ్యాధి గుర్తింపు",
        upload: "ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి",
        class: "మొక్క రకాన్ని ఎంచుకోండి",
        chooseClass: "రకాన్ని ఎంచుకోండి",
        chooseImage: "నమూనా చిత్రాలను చూడటానికి రకాన్ని ఎంచుకోండి.",
        predict: "వ్యాధిని గుర్తించండి",
        camera: "కెమెరాను ఉపయోగించండి",
        voice: "వాయిస్ ద్వారా ప్రశ్న అడగండి",
        voicePlaceholder: "మైక్రోఫోన్ నొక్కి ప్రశ్న అడగండి...",
        speakQuestion: "ప్రశ్న మాట్లాడండి",
        stopInput: "వాయిస్ ఇన్‌పుట్ ఆపండి",
        samples: "ఆకు నమూనా చిత్రాలు",
        plant: "మొక్క",
        disease: "వ్యాధి",
        confidence: "నమ్మక స్థాయి",
        accuracy: "పరీక్ష ఖచ్చితత్వం",
        level: "నమ్మక స్థాయి",
        causes: "వ్యాధి కారణాలు",
        medicine: "మందు / చికిత్స",
        prevention: "నివారణ",
        speak: "ఫలితాన్ని వినండి",
        stopVoice: "వాయిస్ ఆపండి",
        listening: "వింటోంది...",
        processing: "ప్రాసెస్ చేస్తోంది...",
        predictionReady: "వ్యాధి గుర్తింపు పూర్తయింది.",
        noImage: "దయచేసి ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి లేదా ఎంచుకోండి.",
        loading: "లోడ్ అవుతోంది...",
        noSamples: "నమూనా చిత్రాలు అందుబాటులో లేవు."
    },
    ta: {
        ...UI.en,
        language: "மொழி",
        pageTitle: "தாவர நோய் கண்டறிதல்",
        upload: "இலைப் படத்தைப் பதிவேற்றவும்",
        class: "தாவர வகையைத் தேர்ந்தெடுக்கவும்",
        chooseClass: "வகையைத் தேர்ந்தெடுக்கவும்",
        chooseImage: "மாதிரிப் படங்களைப் பார்க்க ஒரு வகையைத் தேர்ந்தெடுக்கவும்.",
        predict: "நோயைக் கண்டறியவும்",
        camera: "கேமராவைப் பயன்படுத்தவும்",
        voice: "குரல் மூலம் கேள்வி கேளுங்கள்",
        voicePlaceholder: "மைக்ரோஃபோனை அழுத்தி கேள்வி கேளுங்கள்...",
        speakQuestion: "கேள்வியைப் பேசவும்",
        stopInput: "குரல் உள்ளீட்டை நிறுத்தவும்",
        samples: "மாதிரி இலைப் படங்கள்",
        plant: "தாவரம்",
        disease: "நோய்",
        confidence: "நம்பிக்கை நிலை",
        accuracy: "சோதனைத் துல்லியம்",
        level: "நம்பிக்கை நிலை",
        causes: "நோய்க்கான காரணங்கள்",
        medicine: "மருந்து / சிகிச்சை",
        prevention: "தடுப்பு",
        speak: "முடிவைக் கேளுங்கள்",
        stopVoice: "குரலை நிறுத்தவும்",
        listening: "கேட்கிறது...",
        processing: "செயலாக்கப்படுகிறது...",
        predictionReady: "நோய் கண்டறிதல் முடிந்தது.",
        noImage: "இலைப் படத்தைப் பதிவேற்றவும் அல்லது தேர்ந்தெடுக்கவும்.",
        loading: "ஏற்றப்படுகிறது...",
        noSamples: "மாதிரிப் படங்கள் இல்லை."
    }
'''

source = source.replace(marker, languages + marker, 1)

# 3. Add a fallback for languages without translated class names.
old = 'CLASS_NAMES[lang][display] || display'
new = '(CLASS_NAMES[lang] || {})[display] || display'
if source.count(old) != 1:
    raise SystemExit("STOP: Class-name lookup was not found exactly once.")
source = source.replace(old, new, 1)

# 4. Make interface language attributes accurate.
old = '''document.documentElement.lang =
        lang === "kn" ? "kn" :
        lang === "hi" ? "hi" : "en";'''
new = '''document.documentElement.lang =
        ["en", "kn", "hi", "mr", "te", "ta"].includes(lang) ? lang : "en";'''
if source.count(old) != 1:
    raise SystemExit("STOP: HTML language assignment was not found.")
source = source.replace(old, new, 1)

# 5. Use English defaults if a UI dictionary is unavailable.
old = 'const t = UI[lang];'
if source.count(old) != 1:
    raise SystemExit("STOP: applyLanguage UI lookup was not found.")
source = source.replace(old, 'const t = UI[lang] || UI.en;', 1)

# 6. Extend translation target selection.
old = '''const targetLanguage =
            target === "kn"
            ? "kn"
            : "hi";'''
new = '''const targetLanguage =
            ["kn", "hi", "mr", "te", "ta"].includes(target)
            ? target
            : "hi";'''
if source.count(old) != 1:
    raise SystemExit("STOP: Frontend translation mapping was not found.")
source = source.replace(old, new, 1)

# 7. Avoid retranslating text already in the target script.
old = '''if (target === "hi" &&
        /[\\u0900-\\u097F]/.test(text)) {
        return text;
    }'''
new = '''if ((target === "hi" || target === "mr") &&
        /[\\u0900-\\u097F]/.test(text)) {
        return text;
    }

    if (target === "te" && /[\\u0C00-\\u0C7F]/.test(text)) {
        return text;
    }

    if (target === "ta" && /[\\u0B80-\\u0BFF]/.test(text)) {
        return text;
    }'''
if source.count(old) != 1:
    raise SystemExit("STOP: Existing script-detection block was not found.")
source = source.replace(old, new, 1)

# 8. Configure speech recognition for all six languages.
old = '''recognition.lang =
        currentLanguage() === "kn"
        ? "kn-IN"
        : currentLanguage() === "hi"
        ? "hi-IN"
        : "en-IN";'''
new = '''const speechLocales = {
        en: "en-IN",
        hi: "hi-IN",
        kn: "kn-IN",
        mr: "mr-IN",
        te: "te-IN",
        ta: "ta-IN"
    };
    recognition.lang = speechLocales[currentLanguage()] || "en-IN";'''
if source.count(old) != 1:
    raise SystemExit("STOP: Speech recognition language mapping was not found.")
source = source.replace(old, new, 1)

if source == original:
    raise SystemExit("STOP: No changes were made.")

path.write_text(source, encoding="utf-8")
print("Frontend updated: six language options, UI dictionaries, translation fallback, and speech locales.")
