
import os
import tempfile
import uuid
from pathlib import Path
from urllib.parse import quote

import edge_tts
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from deep_translator import GoogleTranslator

try:
    from backend.predict import predict_image
except ModuleNotFoundError:
    from predict import predict_image


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
DATASET_DIR = BASE_DIR / "expanded_38_dataset" / "test"
STATIC_DIR = FRONTEND_DIR / "static"

app = FastAPI(title="PlantCare AI", version="2.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if STATIC_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static",
    )


LANGUAGES = {
    "en": {
        "name": "English",
        "voice": "en-IN-NeerjaNeural",
        "labels": {
            "plant": "Plant",
            "disease": "Disease",
            "confidence": "Confidence",
            "accuracy": "Test Accuracy",
            "level": "Confidence Level",
            "causes": "Causes",
            "medicine": "Medicine / Treatment",
            "prevention": "Prevention",
            "high": "High confidence",
            "moderate": "Moderate confidence",
            "low": "Low confidence",
            "speak": "Speak Result",
            "stop": "Stop Voice",
            "loading": "Analyzing image...",
            "error": "Error",
        },
    },
    "hi": {
        "name": "हिन्दी",
        "voice": "hi-IN-SwaraNeural",
        "labels": {
            "plant": "पौधा",
            "disease": "रोग",
            "confidence": "विश्वास स्तर",
            "accuracy": "परीक्षण सटीकता",
            "level": "विश्वास स्तर",
            "causes": "रोग के कारण",
            "medicine": "दवा / उपचार",
            "prevention": "रोकथाम",
            "high": "उच्च विश्वास",
            "moderate": "मध्यम विश्वास",
            "low": "कम विश्वास",
            "speak": "परिणाम सुनें",
            "stop": "आवाज़ रोकें",
            "loading": "चित्र का विश्लेषण हो रहा है...",
            "error": "त्रुटि",
        },
    },
    "kn": {
        "name": "ಕನ್ನಡ",
        "voice": "kn-IN-SapnaNeural",
        "labels": {
            "plant": "ಸಸ್ಯ",
            "disease": "ರೋಗ",
            "confidence": "ವಿಶ್ವಾಸ ಮಟ್ಟ",
            "accuracy": "ಪರೀಕ್ಷಾ ನಿಖರತೆ",
            "level": "ವಿಶ್ವಾಸ ಮಟ್ಟ",
            "causes": "ಕಾರಣಗಳು",
            "medicine": "ಔಷಧಿ / ಚಿಕಿತ್ಸೆ",
            "prevention": "ತಡೆಗಟ್ಟುವಿಕೆ",
            "high": "ಹೆಚ್ಚಿನ ವಿಶ್ವಾಸ",
            "moderate": "ಮಧ್ಯಮ ವಿಶ್ವಾಸ",
            "low": "ಕಡಿಮೆ ವಿಶ್ವಾಸ",
            "speak": "ಫಲಿತಾಂಶವನ್ನು ಕೇಳಿ",
            "stop": "ಧ್ವನಿ ನಿಲ್ಲಿಸಿ",
            "loading": "ಚಿತ್ರವನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...",
            "error": "ದೋಷ",
        },
    },
    "mr": {
        "name": "मराठी",
        "voice": "mr-IN-AarohiNeural",
        "labels": {
            "plant": "वनस्पती",
            "disease": "रोग",
            "confidence": "विश्वास पातळी",
            "accuracy": "चाचणी अचूकता",
            "level": "विश्वास पातळी",
            "causes": "रोगाची कारणे",
            "medicine": "औषध / उपचार",
            "prevention": "प्रतिबंध",
            "high": "उच्च विश्वास",
            "moderate": "मध्यम विश्वास",
            "low": "कमी विश्वास",
            "speak": "निकाल ऐका",
            "stop": "आवाज थांबवा",
            "loading": "प्रतिमेचे विश्लेषण सुरू आहे...",
            "error": "त्रुटी",
        },
    },
    "te": {
        "name": "తెలుగు",
        "voice": "te-IN-ShrutiNeural",
        "labels": {
            "plant": "మొక్క",
            "disease": "వ్యాధి",
            "confidence": "నమ్మక స్థాయి",
            "accuracy": "పరీక్ష ఖచ్చితత్వం",
            "level": "నమ్మక స్థాయి",
            "causes": "వ్యాధి కారణాలు",
            "medicine": "మందు / చికిత్స",
            "prevention": "నివారణ",
            "high": "అధిక నమ్మకం",
            "moderate": "మధ్యస్థ నమ్మకం",
            "low": "తక్కువ నమ్మకం",
            "speak": "ఫలితాన్ని వినండి",
            "stop": "వాయిస్ ఆపండి",
            "loading": "చిత్రాన్ని విశ్లేషిస్తోంది...",
            "error": "లోపం",
        },
    },
    "ta": {
        "name": "தமிழ்",
        "voice": "ta-IN-PallaviNeural",
        "labels": {
            "plant": "தாவரம்",
            "disease": "நோய்",
            "confidence": "நம்பிக்கை நிலை",
            "accuracy": "சோதனை துல்லியம்",
            "level": "நம்பிக்கை நிலை",
            "causes": "நோய்க்கான காரணங்கள்",
            "medicine": "மருந்து / சிகிச்சை",
            "prevention": "தடுப்பு",
            "high": "அதிக நம்பிக்கை",
            "moderate": "மிதமான நம்பிக்கை",
            "low": "குறைந்த நம்பிக்கை",
            "speak": "முடிவைக் கேளுங்கள்",
            "stop": "குரலை நிறுத்து",
            "loading": "படத்தை ஆய்வு செய்கிறது...",
            "error": "பிழை",
        },
    },
}


def translate_text(text, language):
    if not text or language == "en":
        return text

    if language not in LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")

    return GoogleTranslator(
        source="auto",
        target=language,
    ).translate(str(text))


def translate_value(value, language):
    if isinstance(value, str):
        return translate_text(value, language)

    if isinstance(value, list):
        return [
            translate_value(item, language)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            key: translate_value(item, language)
            for key, item in value.items()
        }

    return value


def localize_result(result, language):
    localized = dict(result)

    for key in (
        "plant",
        "disease",
        "cause",
        "causes",
        "medicine",
        "treatment",
        "prevention",
        "suggestions",
        "confidence_level",
        "confidence_message",
    ):
        if key in localized:
            localized[key] = translate_value(
                localized[key],
                language,
            )

    localized["ui"] = LANGUAGES[language]["labels"]
    localized["language"] = language
    return localized


def get_image_files(class_name):
    folder = (DATASET_DIR / class_name).resolve()

    if (
        not folder.is_relative_to(DATASET_DIR.resolve())
        or not folder.is_dir()
    ):
        return []

    return sorted(
        file
        for file in folder.iterdir()
        if file.is_file()
        and file.suffix.lower()
        in {".jpg", ".jpeg", ".png", ".webp"}
    )


@app.get("/")
def home():
    index_file = FRONTEND_DIR / "index.html"

    if not index_file.exists():
        raise HTTPException(
            status_code=404,
            detail="frontend/index.html was not found",
        )

    return FileResponse(index_file)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "PlantCare AI",
    }


@app.get("/api")
def api_info():
    return {
        "service": "PlantCare AI",
        "model": "EfficientNet-B0",
        "test_accuracy": 94.91,
        "classes": 38,
    }


@app.get("/dataset/classes")
@app.get("/api/dataset/classes")
def dataset_classes():
    if not DATASET_DIR.is_dir():
        raise HTTPException(
            status_code=500,
            detail=f"Dataset folder not found: {DATASET_DIR}",
        )

    classes = []

    for folder in sorted(DATASET_DIR.iterdir()):
        if folder.is_dir():
            display = (
                folder.name
                .replace("___", " - ")
                .replace("_", " ")
            )
            classes.append({
                "name": folder.name,
                "display_name": display,
            })

    return {
        "classes": classes,
        "count": len(classes),
    }


@app.get("/dataset/images")
@app.get("/api/dataset/images")
def dataset_images(class_name: str, limit: int = 75):
    available_classes = dataset_classes()["classes"]

    if not any(
        item["name"] == class_name
        for item in available_classes
    ):
        raise HTTPException(
            status_code=404,
            detail="Unknown dataset class",
        )

    files = get_image_files(class_name)[
        :max(1, min(limit, 75))
    ]

    return {
        "images": [
            {
                "filename": file.name,
                "url": (
                    "/dataset-image?class_name="
                    + quote(class_name, safe="")
                    + "&filename="
                    + quote(file.name, safe="")
                ),
            }
            for file in files
        ],
        "count": len(files),
    }


@app.get("/dataset-image")
@app.get("/api/dataset-image")
def dataset_image(class_name: str, filename: str):
    allowed = {
        file.name: file
        for file in get_image_files(class_name)
    }

    file = allowed.get(filename)

    if file is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset image not found",
        )

    return FileResponse(file)


@app.post("/predict")
@app.post("/api/predict")
async def predict(
    image: UploadFile = File(...),
    language: str = Form("en"),
):
    language = (
        language if language in LANGUAGES else "en"
    )

    suffix = Path(
        image.filename or "leaf.jpg"
    ).suffix.lower()

    if suffix not in {
        ".jpg", ".jpeg", ".png", ".webp", ".bmp"
    }:
        suffix = ".jpg"

    content = await image.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded image is empty",
        )

    if len(content) > 15 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Image must be smaller than 15 MB",
        )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp:
            temp.write(content)
            temp_path = temp.name

        # Run the existing trained model.
        result = predict_image(temp_path)

        if (
            not isinstance(result, dict)
            or not result.get("success", False)
        ):
            error = (
                result.get("error", "Prediction failed")
                if isinstance(result, dict)
                else "Prediction failed"
            )
            raise HTTPException(
                status_code=500,
                detail=str(error),
            )

        # Prediction is successful. Translation must not
        # prevent the original result from being returned.
        try:
            return localize_result(result, language)
        except Exception as exc:
            print("Result translation failed:", repr(exc))

            fallback = dict(result)
            fallback["language"] = "en"
            fallback["ui"] = LANGUAGES["en"]["labels"]
            fallback["translation_warning"] = (
                "Translation unavailable. "
                "Showing the result in English."
            )
            return fallback

    except HTTPException:
        raise

    except Exception as exc:
        print("Prediction error:", repr(exc))
        raise HTTPException(
            status_code=500,
            detail=(
                "Prediction failed. "
                "Check the backend terminal."
            ),
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


class TTSRequest(BaseModel):
    text: str
    language: str = "en"



@app.post("/tts")
@app.post("/api/tts")
async def text_to_speech(body: TTSRequest):
    language = (
        body.language
        if body.language in LANGUAGES
        else "en"
    )

    text = (body.text or "").strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="No text provided",
        )

    text = text[:5000]

    output_dir = BASE_DIR / "temp_audio"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{uuid.uuid4().hex}.mp3"

    try:
        voice = LANGUAGES[language]["voice"]

        # The frontend already localizes the result.
        # Do not translate it a second time here.
        communicate = edge_tts.Communicate(
            text,
            voice,
        )

        await communicate.save(str(output_file))

        if not output_file.exists() or output_file.stat().st_size == 0:
            raise RuntimeError("Edge TTS produced an empty audio file.")

        return FileResponse(
            path=str(output_file),
            media_type="audio/mpeg",
            filename="plantcare-result.mp3",
            background=None,
        )

    except Exception as exc:
        print(
            f"TTS error for language={language}, "
            f"voice={LANGUAGES[language]['voice']}: {exc!r}"
        )

        raise HTTPException(
            status_code=502,
            detail=f"Speech generation failed for language '{language}'. "
                   "Check the backend terminal for the TTS error.",
        )


@app.on_event("startup")
async def startup_message():
    print("=" * 50)
    print("PlantCare AI")
    print("Model: EfficientNet-B0")
    print("Reported 38-class test accuracy: 94.91%")
    print("Dataset:", DATASET_DIR)
    print("Dataset available:", DATASET_DIR.is_dir())
    print("=" * 50)
