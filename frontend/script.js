```javascript
"use strict";

// ============================================================
// PLANTCARE AI — MULTILINGUAL FRONTEND
// Languages: English, Hindi, Kannada, Marathi, Tamil, Telugu
// Uses the existing backend API and 38-class prediction model.
// ============================================================

let selectedFile = null;
let currentResult = null;
let cameraStream = null;
let currentAudio = null;
let currentAudioUrl = null;
let recognition = null;
let isListening = false;

const LANGUAGES = {
    en: { locale: "en-IN", name: "English" },
    hi: { locale: "hi-IN", name: "Hindi" },
    kn: { locale: "kn-IN", name: "Kannada" },
    mr: { locale: "mr-IN", name: "Marathi" },
    ta: { locale: "ta-IN", name: "Tamil" },
    te: { locale: "te-IN", name: "Telugu" }
};

const UI = {
    en: {
        selectClass: "-- Select Class --",
        selectImage: "-- Select Test Image --",
        noImage: "No image selected",
        analyze: "Analyze Image",
        cause: "Causes",
        medicine: "Medicine / Treatment",
        treatment: "Treatment",
        prevention: "Prevention",
        confidence: "Confidence",
        confidenceLevel: "Confidence Level",
        accuracy: "Test Accuracy",
        model: "AI Model",
        plant: "Plant",
        disease: "Disease",
        speak: "Speak Result",
        stop: "Stop Voice",
        camera: "Use Camera",
        closeCamera: "Close Camera",
        capture: "Capture Image",
        listening: "Listening...",
        stopListening: "Stop Listening",
        uploadError: "Could not analyze the image.",
        cameraError: "Camera access was not available.",
        speechError: "Speech recognition is not supported by this browser.",
        loading: "Analyzing image...",
        image: "Image",
        high: "High",
        moderate: "Moderate",
        low: "Low",
        language: "Language",
        healthy: "Healthy",
        unknown: "Not available"
    },

    hi: {
        selectClass: "-- वर्ग चुनें --",
        selectImage: "-- परीक्षण छवि चुनें --",
        noImage: "कोई छवि नहीं चुनी गई",
        analyze: "छवि का विश्लेषण करें",
        cause: "कारण",
        medicine: "दवा / उपचार",
        treatment: "उपचार",
        prevention: "रोकथाम",
        confidence: "विश्वास स्तर",
        confidenceLevel: "विश्वास स्तर",
        accuracy: "परीक्षण सटीकता",
        model: "AI मॉडल",
        plant: "पौधा",
        disease: "रोग",
        speak: "परिणाम सुनें",
        stop: "आवाज़ बंद करें",
        camera: "कैमरा उपयोग करें",
        closeCamera: "कैमरा बंद करें",
        capture: "फोटो लें",
        listening: "सुन रहा है...",
        stopListening: "सुनना बंद करें",
        uploadError: "छवि का विश्लेषण नहीं हो सका।",
        cameraError: "कैमरे की अनुमति उपलब्ध नहीं है।",
        speechError: "इस ब्राउज़र में वाक् पहचान समर्थित नहीं है।",
        loading: "छवि का विश्लेषण किया जा रहा है...",
        image: "छवि",
        high: "उच्च",
        moderate: "मध्यम",
        low: "कम",
        language: "भाषा",
        healthy: "स्वस्थ",
        unknown: "उपलब्ध नहीं"
    },

    kn: {
        selectClass: "-- ವರ್ಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ --",
        selectImage: "-- ಪರೀಕ್ಷಾ ಚಿತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ --",
        noImage: "ಯಾವುದೇ ಚಿತ್ರ ಆಯ್ಕೆ ಮಾಡಿಲ್ಲ",
        analyze: "ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        cause: "ಕಾರಣಗಳು",
        medicine: "ಔಷಧಿ / ಚಿಕಿತ್ಸೆ",
        treatment: "ಚಿಕಿತ್ಸೆ",
        prevention: "ತಡೆಗಟ್ಟುವಿಕೆ",
        confidence: "ವಿಶ್ವಾಸ ಮಟ್ಟ",
        confidenceLevel: "ವಿಶ್ವಾಸ ಮಟ್ಟ",
        accuracy: "ಪರೀಕ್ಷಾ ನಿಖರತೆ",
        model: "AI ಮಾದರಿ",
        plant: "ಸಸ್ಯ",
        disease: "ರೋಗ",
        speak: "ಫಲಿತಾಂಶವನ್ನು ಕೇಳಿ",
        stop: "ಧ್ವನಿ ನಿಲ್ಲಿಸಿ",
        camera: "ಕ್ಯಾಮೆರಾ ಬಳಸಿ",
        closeCamera: "ಕ್ಯಾಮೆರಾ ಮುಚ್ಚಿ",
        capture: "ಚಿತ್ರ ತೆಗೆದುಕೊಳ್ಳಿ",
        listening: "ಆಲಿಸಲಾಗುತ್ತಿದೆ...",
        stopListening: "ಆಲಿಸುವುದನ್ನು ನಿಲ್ಲಿಸಿ",
        uploadError: "ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.",
        cameraError: "ಕ್ಯಾಮೆರಾ ಅನುಮತಿ ಲಭ್ಯವಿಲ್ಲ.",
        speechError: "ಈ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಮಾತಿನ ಗುರುತಿಸುವಿಕೆ ಬೆಂಬಲಿತವಾಗಿಲ್ಲ.",
        loading: "ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...",
        image: "ಚಿತ್ರ",
        high: "ಹೆಚ್ಚಿನ",
        moderate: "ಮಧ್ಯಮ",
        low: "ಕಡಿಮೆ",
        language: "ಭಾಷೆ",
        healthy: "ಆರೋಗ್ಯಕರ",
        unknown: "ಲಭ್ಯವಿಲ್ಲ"
    },

    mr: {
        selectClass: "-- वर्ग निवडा --",
        selectImage: "-- चाचणी प्रतिमा निवडा --",
        noImage: "कोणतीही प्रतिमा निवडलेली नाही",
        analyze: "प्रतिमेचे विश्लेषण करा",
        cause: "कारणे",
        medicine: "औषध / उपचार",
        treatment: "उपचार",
        prevention: "प्रतिबंध",
        confidence: "विश्वास पातळी",
        confidenceLevel: "विश्वास पातळी",
        accuracy: "चाचणी अचूकता",
        model: "AI मॉडेल",
        plant: "वनस्पती",
        disease: "रोग",
        speak: "निकाल ऐका",
        stop: "आवाज बंद करा",
        camera: "कॅमेरा वापरा",
        closeCamera: "कॅमेरा बंद करा",
        capture: "प्रतिमा काढा",
        listening: "ऐकत आहे...",
        stopListening: "ऐकणे थांबवा",
        uploadError: "प्रतिमेचे विश्लेषण करता आले नाही.",
        cameraError: "कॅमेऱ्याची परवानगी उपलब्ध नाही.",
        speechError: "या ब्राउझरमध्ये वाक् ओळख उपलब्ध नाही.",
        loading: "प्रतिमेचे विश्लेषण सुरू आहे...",
        image: "प्रतिमा",
        high: "उच्च",
        moderate: "मध्यम",
        low: "कमी",
        language: "भाषा",
        healthy: "निरोगी",
        unknown: "उपलब्ध नाही"
    },

    ta: {
        selectClass: "-- வகையைத் தேர்ந்தெடுக்கவும் --",
        selectImage: "-- சோதனைப் படத்தைத் தேர்ந்தெடுக்கவும் --",
        noImage: "படம் தேர்ந்தெடுக்கப்படவில்லை",
        analyze: "படத்தைப் பகுப்பாய்வு செய்",
        cause: "காரணங்கள்",
        medicine: "மருந்து / சிகிச்சை",
        treatment: "சிகிச்சை",
        prevention: "தடுப்பு",
        confidence: "நம்பகத்தன்மை",
        confidenceLevel: "நம்பகத்தன்மை நிலை",
        accuracy: "சோதனைத் துல்லியம்",
        model: "AI மாதிரி",
        plant: "தாவரம்",
        disease: "நோய்",
        speak: "முடிவைக் கேளுங்கள்",
        stop: "குரலை நிறுத்து",
        camera: "கேமராவைப் பயன்படுத்து",
        closeCamera: "கேமராவை மூடு",
        capture: "படம் எடு",
        listening: "கேட்கிறது...",
        stopListening: "கேட்பதை நிறுத்து",
        uploadError: "படத்தைப் பகுப்பாய்வு செய்ய முடியவில்லை.",
        cameraError: "கேமரா அனுமதி கிடைக்கவில்லை.",
        speechError: "இந்த உலாவியில் பேச்சு அடையாளம் காணுதல் ஆதரிக்கப்படவில்லை.",
        loading: "படம் பகுப்பாய்வு செய்யப்படுகிறது...",
        image: "படம்",
        high: "உயர்",
        moderate: "மிதமான",
        low: "குறைந்த",
        language: "மொழி",
        healthy: "ஆரோக்கியமான",
        unknown: "கிடைக்கவில்லை"
    },

    te: {
        selectClass: "-- వర్గాన్ని ఎంచుకోండి --",
        selectImage: "-- పరీక్ష చిత్రాన్ని ఎంచుకోండి --",
        noImage: "చిత్రం ఎంచుకోలేదు",
        analyze: "చిత్రాన్ని విశ్లేషించండి",
        cause: "కారణాలు",
        medicine: "మందు / చికిత్స",
        treatment: "చికిత్స",
        prevention: "నివారణ",
        confidence: "నమ్మక స్థాయి",
        confidenceLevel: "నమ్మక స్థాయి",
        accuracy: "పరీక్ష ఖచ్చితత్వం",
        model: "AI మోడల్",
        plant: "మొక్క",
        disease: "వ్యాధి",
        speak: "ఫలితాన్ని వినండి",
        stop: "వాయిస్ ఆపండి",
        camera: "కెమెరాను ఉపయోగించండి",
        closeCamera: "కెమెరాను మూసివేయండి",
        capture: "చిత్రాన్ని తీయండి",
        listening: "వింటోంది...",
        stopListening: "వినడం ఆపండి",
        uploadError: "చిత్రాన్ని విశ్లేషించలేకపోయాము.",
        cameraError: "కెమెరా అనుమతి అందుబాటులో లేదు.",
        speechError: "ఈ బ్రౌజర్‌లో మాట గుర్తింపు అందుబాటులో లేదు.",
        loading: "చిత్రాన్ని విశ్లేషిస్తోంది...",
        image: "చిత్రం",
        high: "అధిక",
        moderate: "మధ్యస్థ",
        low: "తక్కువ",
        language: "భాష",
        healthy: "ఆరోగ్యకరమైన",
        unknown: "అందుబాటులో లేదు"
    }
};

function el(...ids) {
    for (const id of ids) {
        const node = document.getElementById(id);
        if (node) return node;
    }
    return null;
}

function setText(ids, value) {
    const node = el(...ids);
    if (node) node.textContent = value == null ? "" : String(value);
}

function getUI() {
    return UI[selectedLanguage] || UI.en;
}

function getLocale() {
    return (LANGUAGES[selectedLanguage] || LANGUAGES.en).locale;
}

function getDisplayName(className) {
    if (!className) return "";
    return className
        .replace(/___/g, " - ")
        .replace(/_/g, " ")
        .replace(/\s+/g, " ")
        .trim();
}

function formatPercent(value) {
    const number = Number(value);
    return Number.isFinite(number) ? `${number.toFixed(2)}%` : "—";
}

function setLoading(visible) {
    const node = el("loading", "loader", "loadingMessage");
    if (!node) return;
    node.style.display = visible ? "block" : "none";
    if (visible) node.textContent = getUI().loading;
}

function getErrorMessage(data, fallback) {
    if (data && typeof data.detail === "string") return data.detail;
    if (data && typeof data.message === "string") return data.message;
    return fallback;
}

// ============================================================
// LANGUAGE SELECTOR
// ============================================================

function setupLanguage() {
    const select = el("languageSelect", "language", "langSelect");
    if (!select) return;

    const existing = select.value;
    if (LANGUAGES[existing]) selectedLanguage = existing;

    // Ensure all six language choices are present.
    const labels = {
        en: "English",
        hi: "हिन्दी",
        kn: "ಕನ್ನಡ",
        mr: "मराठी",
        ta: "தமிழ்",
        te: "తెలుగు"
    };

    const present = new Set(
        Array.from(select.options).map(option => option.value)
    );

    for (const [code, label] of Object.entries(labels)) {
        if (!present.has(code)) {
            const option = document.createElement("option");
            option.value = code;
            option.textContent = label;
            select.appendChild(option);
        }
    }

    if (!LANGUAGES[select.value]) select.value = selectedLanguage;

    select.addEventListener("change", () => {
        selectedLanguage = LANGUAGES[select.value] ? select.value : "en";
        stopVoice();
        updateUILanguage();
        reloadClassNames();

        if (currentResult) displayResult(currentResult);

        if (selectedFile) {
            // Re-run the prediction with the newly selected language
            // so the backend can localize the response.
            predictImage(selectedFile);
        }
    });
}

// ============================================================
// CLASS LIST AND TEST IMAGES
// ============================================================

async function loadClasses() {
    const select = el("classSelect", "diseaseClass", "classSelector", "plantClass");
    if (!select) return;

    try {
        const response = await fetch("/dataset/classes");
        const data = await response.json();

        if (!response.ok) {
            throw new Error(getErrorMessage(data, "Could not load classes."));
        }

        select.innerHTML = "";
        const placeholder = document.createElement("option");
        placeholder.value = "";
        placeholder.textContent = getUI().selectClass;
        select.appendChild(placeholder);

        const classes = Array.isArray(data.classes) ? data.classes : [];

        for (const item of classes) {
            const className =
                typeof item === "string" ? item :
                item.name || item.class_name || item.value || "";

            if (!className) continue;

            const option = document.createElement("option");
            option.value = className;
            option.textContent = getDisplayName(className);
            select.appendChild(option);
        }

        select.removeEventListener("change", loadImagesForClass);
        select.addEventListener("change", loadImagesForClass);
    } catch (error) {
        console.error("Class loading error:", error);
    }
}

async function loadImagesForClass(event) {
    const className = event.target.value;
    const imageSelect = el("imageSelect", "testImageSelect", "datasetImage", "testImage");
    if (!imageSelect) return;

    imageSelect.innerHTML = "";
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = getUI().selectImage;
    imageSelect.appendChild(placeholder);

    if (!className) return;

    try {
        const response = await fetch("/dataset/images/" + encodeURIComponent(className));
        const data = await response.json();

        if (!response.ok) {
            throw new Error(getErrorMessage(data, "Could not load test images."));
        }

        for (const [index, image] of (data.images || []).entries()) {
            const option = document.createElement("option");
            option.value = image.url || image.path || "";
            option.textContent = `${getUI().image} ${index + 1} - ${image.filename || ""}`;
            imageSelect.appendChild(option);
        }

        imageSelect.onchange = function () {
            if (this.value) showDatasetImage(this.value);
        };
    } catch (error) {
        console.error("Image loading error:", error);
    }
}

function showDatasetImage(url) {
    const preview = el("imagePreview", "previewImage", "selectedImage", "plantImagePreview");
    if (!preview) return;

    preview.src = url;
    preview.style.display = "block";
    preview.onerror = () => console.error("Could not display dataset image:", url);
}

// ============================================================
// IMAGE UPLOAD AND PREVIEW
// ============================================================

function setupUpload() {
    const input = el("imageInput", "fileInput", "uploadInput", "plantImage");
    const button = el("uploadButton", "uploadBtn", "chooseImageButton");

    if (button && input) button.onclick = () => input.click();

    if (input) {
        input.addEventListener("change", function () {
            const file = this.files && this.files[0];
            if (!file) return;

            if (!file.type.startsWith("image/")) {
                alert("Please select an image file.");
                return;
            }

            selectedFile = file;
            showSelectedFile(file);
            showUploadedImage(file);
            predictImage(file);
        });
    }
}

function showSelectedFile(file) {
    setText(["fileName", "selectedFileName"], file ? file.name : getUI().noImage);
}

function showUploadedImage(file) {
    const preview = el("imagePreview", "previewImage", "selectedImage", "plantImagePreview");
    if (!preview || !file) return;

    if (preview.dataset.objectUrl) {
        URL.revokeObjectURL(preview.dataset.objectUrl);
    }

    const url = URL.createObjectURL(file);
    preview.dataset.objectUrl = url;
    preview.src = url;
    preview.style.display = "block";
}

// ============================================================
// PREDICTION
// ============================================================

async function predictImage(file) {
    if (!file) return;

    stopVoice();
    setLoading(true);

    try {
        const formData = new FormData();
        formData.append("image", file);
        formData.append("language", selectedLanguage);

        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(getErrorMessage(result, getUI().uploadError));
        }

        currentResult = result;
        displayResult(result);
    } catch (error) {
        console.error("Prediction error:", error);
        alert(error.message || getUI().uploadError);
    } finally {
        setLoading(false);
    }
}

// ============================================================
// RESULT DISPLAY
// ============================================================

function getResultField(result, keys, fallback = "") {
    for (const key of keys) {
        if (result[key] !== undefined && result[key] !== null && result[key] !== "") {
            return result[key];
        }
    }
    return fallback;
}

function displayResult(result) {
    if (!result) return;

    const className = getResultField(result, ["predicted_class", "class_name", "class"], "");
    const disease = getResultField(result, ["disease", "disease_name", "display_name"], getDisplayName(className));
    const plant = getResultField(result, ["plant", "plant_name"], "");
    const cause = getResultField(result, ["cause", "causes"], getUI().unknown);
    const medicine = getResultField(result, ["medicine", "treatment", "recommended_medicine"], getUI().unknown);
    const prevention = getResultField(result, ["prevention", "suggestions"], getUI().unknown);
    const confidence = getResultField(result, ["confidence"], 0);
    const accuracy = getResultField(result, ["test_accuracy", "accuracy"], 94.91);
    const modelName = getResultField(result, ["model_name", "model"], "EfficientNet-B0");

    setText(["diseaseName", "disease", "predictionDisease", "resultDisease"], disease);
    setText(["plantName", "plant", "predictionPlant", "resultPlant"], plant);
    setText(["confidence", "confidenceValue", "predictionConfidence"], formatPercent(confidence));
    setText(["testAccuracy", "accuracy", "modelAccuracy"], formatPercent(accuracy));
    setText(["modelName", "model"], modelName);
    setText(["cause", "causeText"], cause);
    setText(["medicine", "medicineText", "recommendedMedicine", "medicineRecommendation"], medicine);
    setText(["treatment", "treatmentText"], medicine);
    setText(["prevention", "preventionText", "suggestions"], prevention);

    const confidenceNumber = Number(confidence);
    let confidenceLabel = getUI().low;

    if (confidenceNumber >= 70) confidenceLabel = getUI().high;
    else if (confidenceNumber >= 50) confidenceLabel = getUI().moderate;

    setText(["confidenceLevel"], confidenceLabel);

    const resultArea = el("result", "results", "resultSection");
    if (resultArea) {
        resultArea.style.display = "block";
        resultArea.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    const speakButton = el("speakButton", "speakBtn", "voiceButton");
    if (speakButton) {
        speakButton.style.display = "inline-block";
        speakButton.textContent = "🔊 " + getUI().speak;
        speakButton.onclick = speakResult;
    }

    const stopButton = el("stopVoiceButton", "stopButton", "stopVoice");
    if (stopButton) {
        stopButton.textContent = "■ " + getUI().stop;
        stopButton.onclick = stopVoice;
    }
}

// ============================================================
// BUILD SPEECH TEXT
// Prefer backend-localized values from the current prediction.
// ============================================================

function buildSpeechText(result) {
    const u = getUI();
    const parts = [
        `${u.plant}: ${getResultField(result, ["plant", "plant_name"], "")}`,
        `${u.disease}: ${getResultField(result, ["disease", "disease_name", "display_name", "predicted_class"], "")}`,
        `${u.confidence}: ${Number(getResultField(result, ["confidence"], 0)).toFixed(2)} percent`,
        `${u.cause}: ${getResultField(result, ["cause", "causes"], "")}`,
        `${u.medicine}: ${getResultField(result, ["medicine", "treatment", "recommended_medicine"], "")}`,
        `${u.prevention}: ${getResultField(result, ["prevention", "suggestions"], "")}`
    ];

    return parts.filter(part => !part.endsWith(": ")).join(". ");
}

// ============================================================
// TEXT TO SPEECH
// Backend should return audio for the requested language.
// ============================================================

async function speakResult() {
    if (!currentResult) return;

    stopVoice();

    const text = buildSpeechText(currentResult);
    if (!text.trim()) return;

    try {
        const formData = new FormData();
        formData.append("text", text);
        formData.append("language", selectedLanguage);

        const response = await fetch("/tts", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Backend text-to-speech failed.");
        }

        const blob = await response.blob();

        if (!blob.size) {
            throw new Error("The backend returned empty audio.");
        }

        currentAudioUrl = URL.createObjectURL(blob);
        currentAudio = new Audio(currentAudioUrl);

        currentAudio.onended = () => {
            if (currentAudioUrl) URL.revokeObjectURL(currentAudioUrl);
            currentAudioUrl = null;
            currentAudio = null;
        };

        await currentAudio.play();
    } catch (error) {
        console.error("TTS error:", error);

        // Browser fallback only speaks the text it receives;
        // it does not translate English text into another language.
        if ("speechSynthesis" in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = getLocale();

            const voices = window.speechSynthesis.getVoices();
            const matchingVoice = voices.find(voice =>
                voice.lang.toLowerCase() === getLocale().toLowerCase()
            );

            if (matchingVoice) utterance.voice = matchingVoice;

            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
        } else {
            alert("Text-to-speech is not supported in this browser.");
        }
    }
}

function stopVoice() {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }

    if (currentAudioUrl) {
        URL.revokeObjectURL(currentAudioUrl);
        currentAudioUrl = null;
    }

    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
    }
}

// ============================================================
// MICROPHONE INPUT
// Uses the selected language's browser speech-recognition locale.
// ============================================================

function stopListening() {
    if (recognition) {
        try {
            recognition.stop();
        } catch (_) {
            // Recognition may already have stopped.
        }
    }

    recognition = null;
    isListening = false;

    const button = el("voiceInputButton", "micButton", "startListeningButton");
    if (button) button.textContent = "🎤 " + (getUI().listen || "Voice Input");
}

function startListening() {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert(getUI().speechError);
        return;
    }

    stopListening();

    recognition = new SpeechRecognition();
    recognition.lang = getLocale();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    isListening = true;

    const button = el("voiceInputButton", "micButton", "startListeningButton");
    if (button) button.textContent = "🎤 " + getUI().listening;

    recognition.onresult = event => {
        const transcript = event.results?.[0]?.[0]?.transcript || "";
        const input = el("voiceCommand", "searchInput", "questionInput", "chatInput");

        if (input) {
            input.value = transcript;
            input.dispatchEvent(new Event("input", { bubbles: true }));
            input.dispatchEvent(new Event("change", { bubbles: true }));
        } else {
            // No voice-command API is assumed. Show recognized text for the user.
            alert(transcript);
        }
    };

    recognition.onerror = event => {
        console.error("Speech recognition error:", event.error);
        if (event.error !== "no-speech" && event.error !== "aborted") {
            alert("Microphone input failed: " + event.error);
        }
    };

    recognition.onend = () => {
        recognition = null;
        isListening = false;

        const micButton = el("voiceInputButton", "micButton", "startListeningButton");
        if (micButton) micButton.textContent = "🎤 " + (getUI().listen || "Voice Input");
    };

    try {
        recognition.start();
    } catch (error) {
        console.error("Could not start speech recognition:", error);
        stopListening();
    }
}

function setupVoiceInput() {
    const button = el("voiceInputButton", "micButton", "startListeningButton");
    if (!button) return;

    button.onclick = () => {
        if (isListening) stopListening();
        else startListening();
    };
}

// ============================================================
// UPDATE UI LABELS
// ============================================================

function updateUILanguage() {
    const u = getUI();

    setText(["causeTitle"], u.cause);
    setText(["medicineTitle"], u.medicine);
    setText(["treatmentTitle"], u.treatment);
    setText(["preventionTitle"], u.prevention);
    setText(["confidenceTitle"], u.confidence);
    setText(["accuracyTitle"], u.accuracy);
    setText(["modelTitle"], u.model);
    setText(["plantTitle"], u.plant);
    setText(["diseaseTitle"], u.disease);
    setText(["speakButton", "speakBtn", "voiceButton"], "🔊 " + u.speak);
    setText(["stopVoiceButton", "stopButton", "stopVoice"], "■ " + u.stop);
    setText(["cameraButton", "cameraBtn", "useCamera"], "📷 " + u.camera);
    setText(["captureButton", "captureBtn"], "📸 " + u.capture);

    const classSelect = el("classSelect", "diseaseClass", "classSelector", "plantClass");
    if (classSelect?.options?.length) {
        classSelect.options[0].textContent = u.selectClass;
    }

    const imageSelect = el("imageSelect", "testImageSelect", "datasetImage", "testImage");
    if (imageSelect?.options?.length) {
        imageSelect.options[0].textContent = u.selectImage;
    }

    setLoading(false);
}

function reloadClassNames() {
    const select = el("classSelect", "diseaseClass", "classSelector", "plantClass");
    if (!select) return;

    for (const option of Array.from(select.options)) {
        if (option.value) option.textContent = getDisplayName(option.value);
    }
}

// ============================================================
// CAMERA
// ============================================================

function setupCamera() {
    const cameraButton = el("cameraButton", "cameraBtn", "useCamera");
    const captureButton = el("captureButton", "captureBtn");
    const video = el("cameraVideo", "video");
    const canvas = el("cameraCanvas", "canvas");

    if (cameraButton && video) {
        cameraButton.onclick = async function () {
            if (cameraStream) {
                cameraStream.getTracks().forEach(track => track.stop());
                cameraStream = null;
                video.srcObject = null;
                video.style.display = "none";
                if (captureButton) captureButton.style.display = "none";
                cameraButton.textContent = "📷 " + getUI().camera;
                return;
            }

            try {
                cameraStream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = cameraStream;
                video.style.display = "block";
                await video.play();

                if (captureButton) {
                    captureButton.style.display = "inline-block";
                    captureButton.textContent = "📸 " + getUI().capture;
                }

                cameraButton.textContent = "📷 " + getUI().closeCamera;
            } catch (error) {
                console.error("Camera error:", error);
                alert(getUI().cameraError);
            }
        };
    }

    if (captureButton && video && canvas) {
        captureButton.onclick = function () {
            if (!video.videoWidth || !video.videoHeight) {
                alert("Wait for the camera to start.");
                return;
            }

            const context = canvas.getContext("2d");
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            canvas.toBlob(blob => {
                if (!blob) return;

                selectedFile = new File([blob], "camera_plant.jpg", {
                    type: "image/jpeg"
                });

                showSelectedFile(selectedFile);
                showUploadedImage(selectedFile);
                predictImage(selectedFile);
            }, "image/jpeg", 0.95);
        };
    }
}

// ============================================================
// RANDOM TEST IMAGE
// ============================================================

function setupRandomImage() {
    const randomButton = el("randomButton", "randomBtn", "selectRandomImage");
    if (!randomButton) return;

    randomButton.onclick = async function () {
        const classSelect = el("classSelect", "diseaseClass", "classSelector", "plantClass");
        const imageSelect = el("imageSelect", "testImageSelect", "datasetImage", "testImage");

        if (!classSelect || !imageSelect) return;

        const options = Array.from(classSelect.options).filter(option => option.value);
        if (!options.length) return;

        classSelect.value = options[Math.floor(Math.random() * options.length)].value;

        await loadImagesForClass({ target: classSelect });

        const imageOptions = Array.from(imageSelect.options).filter(option => option.value);
        if (!imageOptions.length) return;

        const imageOption = imageOptions[Math.floor(Math.random() * imageOptions.length)];
        imageSelect.value = imageOption.value;
        showDatasetImage(imageOption.value);
    };
}

// ============================================================
// INITIALIZATION
// ============================================================

document.addEventListener("DOMContentLoaded", async () => {
    console.log("PlantCare AI multilingual frontend started.");

    setupLanguage();
    updateUILanguage();
    setupUpload();
    setupCamera();
    setupRandomImage();
    setupVoiceInput();

    await loadClasses();

    const languageSelect = el("languageSelect", "language", "langSelect");
    if (languageSelect && LANGUAGES[languageSelect.value]) {
        selectedLanguage = languageSelect.value;
    }

    updateUILanguage();
    reloadClassNames();

    if (currentResult) displayResult(currentResult);
});

window.addEventListener("beforeunload", () => {
    stopVoice();

    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
    }
});
```