from pathlib import Path
from datetime import datetime

path = Path("frontend/index.html")
original = path.read_text(encoding="utf-8")

start_marker = "async function speakResult() {"
end_marker = "speakButton.addEventListener("

start = original.find(start_marker)
end = original.find(end_marker, start + len(start_marker))

if start < 0 or end < 0:
    raise SystemExit(
        "STOP: Could not locate the complete function. No file was changed."
    )

backup = path.with_name(
    f"index.html.backup-{datetime.now():%Y%m%d-%H%M%S}"
)
backup.write_text(original, encoding="utf-8")

replacement = r'''function speechText(value) {
    if (value === null || value === undefined) return "";
    if (Array.isArray(value)) {
        return value.map(speechText).filter(Boolean).join(". ");
    }
    if (typeof value === "object") {
        return Object.values(value).map(speechText).filter(Boolean).join(". ");
    }
    return String(value).trim();
}

async function speakResult() {
    if (!latestResult) {
        showError(UI[currentLanguage()].noImage);
        return;
    }

    const lang = currentLanguage();
    const t = UI[lang] || UI.en;
    let audioUrl = null;

    try {
        const localized = await localizeResult(latestResult);
        const parts = [];

        function addSection(label, value) {
            const content = speechText(value);
            if (content) parts.push(`${label}. ${content}.`);
        }

        addSection(t.plant || "Plant", localized.plant);
        addSection(t.disease || "Disease", localized.disease);

        if (localized.confidence !== undefined &&
            localized.confidence !== null) {
            addSection(
                t.confidence || "Confidence",
                formatPercent(localized.confidence)
            );
        }

        if (localized.test_accuracy !== undefined &&
            localized.test_accuracy !== null) {
            addSection(
                t.accuracy || "Test accuracy",
                formatPercent(localized.test_accuracy)
            );
        }

        addSection(
            t.level || "Confidence level",
            localized.confidence_level
        );
        addSection(t.causes || "Causes", localized.causes || localized.cause);
        addSection(
            t.medicine || "Treatment",
            localized.medicine || localized.treatment
        );
        addSection(t.prevention || "Prevention", localized.prevention);
        addSection(
            t.recommendations || "Recommendations",
            localized.suggestions || localized.recommendations
        );

        const speech = parts.join(" ");

        if (!speech.trim()) {
            showError("No result advice is available to read aloud.");
            return;
        }

        console.log("PlantCare AI speech text:", speech);

        try {
            const response = await fetch(`${API}/tts`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    text: speech,
                    language: lang
                })
            });

            if (!response.ok) {
                throw new Error(`TTS server returned HTTP ${response.status}`);
            }

            const blob = await response.blob();

            if (!blob.size) {
                throw new Error("The TTS server returned empty audio.");
            }

            audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);

            audio.addEventListener("ended", () => {
                URL.revokeObjectURL(audioUrl);
            }, { once: true });

            audio.addEventListener("error", () => {
                URL.revokeObjectURL(audioUrl);
            }, { once: true });

            await audio.play();
            return;
        } catch (error) {
            console.warn(
                "Backend voice playback failed; trying browser speech:",
                error
            );

            if (audioUrl) {
                URL.revokeObjectURL(audioUrl);
                audioUrl = null;
            }
        }

        if (!("speechSynthesis" in window)) {
            showError("Voice playback is not supported in this browser.");
            return;
        }

        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(speech);
        const locales = {
            en: "en-IN",
            hi: "hi-IN",
            kn: "kn-IN",
            mr: "mr-IN",
            te: "te-IN",
            ta: "ta-IN"
        };

        utterance.lang = locales[lang] || "en-IN";
        utterance.rate = 0.9;

        utterance.onerror = (event) => {
            console.error("Browser speech error:", event.error);
        };

        window.speechSynthesis.speak(utterance);
    } catch (error) {
        console.error("Speak Result failed:", error);
        showError("Voice output failed. Check the browser console and backend terminal.");
    }
}

'''

updated = original[:start] + replacement + original[end:]
path.write_text(updated, encoding="utf-8")

print("Voice function updated.")
print(f"Backup saved at: {backup}")
print("Next: refresh the PlantCare AI webpage and test Speak Result.")
