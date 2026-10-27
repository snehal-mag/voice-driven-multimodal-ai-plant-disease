"use strict";


// ============================================================
// GLOBAL VARIABLES
// ============================================================

let selectedFile = null;
let currentResult = null;
let selectedLanguage = "en";
let cameraStream = null;


// ============================================================
// 30 CLASS INFORMATION
// ============================================================

const INFO = {

    "Apple___Apple_scab": {
        en: ["Apple Scab", "Apple", "Venturia inaequalis fungus.", "Use a registered apple scab fungicide according to the product label.", "Remove fallen leaves and maintain good air circulation."],
        hi: ["सेब स्कैब रोग", "सेब", "Venturia inaequalis फंगस।", "उत्पाद के लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "गिरी हुई पत्तियों को हटाएं और अच्छा वायु संचार रखें।"],
        kn: ["ಸೇಬಿನ ಸ್ಕ್ಯಾಬ್ ರೋಗ", "ಸೇಬು", "Venturia inaequalis ಶಿಲೀಂಧ್ರ.", "ಉತ್ಪನ್ನದ ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ.", "ಬಿದ್ದ ಎಲೆಗಳನ್ನು ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಉತ್ತಮ ಗಾಳಿಯ ಸಂಚಾರವನ್ನು ಕಾಪಾಡಿ."]
    },

    "Apple___Black_rot": {
        en: ["Apple Black Rot", "Apple", "Botryosphaeria obtusa fungus.", "Use a fungicide registered for apple black rot according to the product label.", "Remove infected fruits and branches."],
        hi: ["सेब ब्लैक रॉट", "सेब", "Botryosphaeria obtusa फंगस।", "उत्पाद के लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "संक्रमित फल और शाखाएं हटाएं।"],
        kn: ["ಸೇಬಿನ ಕಪ್ಪು ಕೊಳೆ ರೋಗ", "ಸೇಬು", "Botryosphaeria obtusa ಶಿಲೀಂಧ್ರ.", "ಉತ್ಪನ್ನದ ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ.", "ಸೋಂಕಿತ ಹಣ್ಣುಗಳು ಮತ್ತು ಕೊಂಬೆಗಳನ್ನು ತೆಗೆದುಹಾಕಿ."]
    },

    "Apple___Cedar_apple_rust": {
        en: ["Apple Cedar Rust", "Apple", "Gymnosporangium fungus.", "Use a fungicide registered for cedar apple rust according to the product label.", "Maintain orchard sanitation and monitor plants."],
        hi: ["सेब सीडर रस्ट", "सेब", "Gymnosporangium फंगस।", "उत्पाद के लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "बगीचे की स्वच्छता बनाए रखें।"],
        kn: ["ಸೇಬಿನ ಸೀಡರ್ ರಸ್ಟ್", "ಸೇಬು", "Gymnosporangium ಶಿಲೀಂಧ್ರ.", "ಉತ್ಪನ್ನದ ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ.", "ತೋಟದ ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿ."]
    },

    "Apple___healthy": {
        en: ["Healthy Apple", "Apple", "No visible disease symptoms.", "No medicine required.", "Continue proper watering, nutrition and monitoring."],
        hi: ["स्वस्थ सेब", "सेब", "बीमारी के कोई स्पष्ट लक्षण नहीं।", "किसी दवा की आवश्यकता नहीं है।", "उचित सिंचाई, पोषण और निगरानी जारी रखें।"],
        kn: ["ಆರೋಗ್ಯಕರ ಸೇಬು", "ಸೇಬು", "ರೋಗದ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಲಕ್ಷಣಗಳಿಲ್ಲ.", "ಯಾವುದೇ ಔಷಧಿಯ ಅಗತ್ಯವಿಲ್ಲ.", "ಸರಿಯಾದ ನೀರಾವರಿ, ಪೋಷಕಾಂಶ ಮತ್ತು ಪರಿಶೀಲನೆ ಮುಂದುವರಿಸಿ."]
    },

    "Blueberry___healthy": {
        en: ["Healthy Blueberry", "Blueberry", "No visible disease symptoms.", "No medicine required.", "Maintain proper irrigation and nutrition."],
        hi: ["स्वस्थ ब्लूबेरी", "ब्लूबेरी", "बीमारी के कोई स्पष्ट लक्षण नहीं।", "किसी दवा की आवश्यकता नहीं है।", "उचित सिंचाई और पोषण बनाए रखें।"],
        kn: ["ಆರೋಗ್ಯಕರ ಬ್ಲೂಬೆರಿ", "ಬ್ಲೂಬೆರಿ", "ರೋಗದ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಲಕ್ಷಣಗಳಿಲ್ಲ.", "ಯಾವುದೇ ಔಷಧಿಯ ಅಗತ್ಯವಿಲ್ಲ.", "ಸರಿಯಾದ ನೀರಾವರಿ ಮತ್ತು ಪೋಷಕಾಂಶ ಕಾಪಾಡಿ."]
    },

    "Cherry_(including_sour)___Powdery_mildew": {
        en: ["Cherry Powdery Mildew", "Cherry", "Fungal infection causing powdery growth.", "Use a registered fungicide according to the product label.", "Improve air circulation and avoid excess moisture."],
        hi: ["चेरी पाउडरी मिल्ड्यू", "चेरी", "पाउडर जैसी परत बनाने वाला फंगल संक्रमण।", "उत्पाद के लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "वायु संचार बेहतर रखें और अधिक नमी से बचें।"],
        kn: ["ಚೆರ್ರಿ ಪೌಡರಿ ಮಿಲ್ಡ್ಯೂ", "ಚೆರ್ರಿ", "ಪುಡಿಯಂತಹ ಪದರ ಉಂಟುಮಾಡುವ ಶಿಲೀಂಧ್ರ ಸೋಂಕು.", "ಉತ್ಪನ್ನದ ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ.", "ಉತ್ತಮ ಗಾಳಿಯ ಸಂಚಾರವನ್ನು ಕಾಪಾಡಿ."]
    },

    "Cherry_(including_sour)___healthy": {
        en: ["Healthy Cherry", "Cherry", "No visible disease symptoms.", "No medicine required.", "Maintain irrigation, nutrition and sanitation."],
        hi: ["स्वस्थ चेरी", "चेरी", "बीमारी के कोई स्पष्ट लक्षण नहीं।", "किसी दवा की आवश्यकता नहीं है।", "सिंचाई, पोषण और स्वच्छता बनाए रखें।"],
        kn: ["ಆರೋಗ್ಯಕರ ಚೆರ್ರಿ", "ಚೆರ್ರಿ", "ರೋಗದ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಲಕ್ಷಣಗಳಿಲ್ಲ.", "ಯಾವುದೇ ಔಷಧಿಯ ಅಗತ್ಯವಿಲ್ಲ.", "ನೀರಾವರಿ, ಪೋಷಕಾಂಶ ಮತ್ತು ಸ್ವಚ್ಛತೆ ಕಾಪಾಡಿ."]
    },

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        en: ["Corn Gray Leaf Spot", "Corn", "Cercospora fungus.", "Use a fungicide registered for corn gray leaf spot according to the label.", "Use crop rotation and resistant varieties."],
        hi: ["मक्का ग्रे लीफ स्पॉट", "मक्का", "Cercospora फंगस।", "लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "फसल चक्र और प्रतिरोधी किस्मों का उपयोग करें।"],
        kn: ["ಮಕ್ಕಿಯ ಗ್ರೇ ಲೀಫ್ ಸ್ಪಾಟ್", "ಮಕ್ಕಿ", "Cercospora ಶಿಲೀಂಧ್ರ.", "ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ.", "ಬೆಳೆ ಪರಿವರ್ತನೆ ಮತ್ತು ರೋಗ ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ."]
    },

    "Corn_(maize)___Common_rust_": {
        en: ["Corn Common Rust", "Corn", "Puccinia fungus.", "Use a fungicide registered for corn rust according to the label.", "Use resistant varieties and monitor regularly."],
        hi: ["मक्का कॉमन रस्ट", "मक्का", "Puccinia फंगस।", "लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "प्रतिरोधी किस्मों का उपयोग करें।"],
        kn: ["ಮಕ್ಕಿಯ ಸಾಮಾನ್ಯ ರಸ್ಟ್", "ಮಕ್ಕಿ", "Puccinia ಶಿಲೀಂಧ್ರ.", "ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ.", "ರೋಗ ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ."]
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        en: ["Corn Northern Leaf Blight", "Corn", "Exserohilum turcicum fungus.", "Use a fungicide registered for corn leaf blight according to the label.", "Use resistant varieties and crop rotation."],
        hi: ["मक्का नॉर्दर्न लीफ ब्लाइट", "मक्का", "Exserohilum turcicum फंगस।", "लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "प्रतिरोधी किस्मों और फसल चक्र का उपयोग करें।"],
        kn: ["ಮಕ್ಕಿಯ ನಾರ್ದರ್ನ್ ಲೀಫ್ ಬ್ಲೈಟ್", "ಮಕ್ಕಿ", "Exserohilum turcicum ಶಿಲೀಂಧ್ರ.", "ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ.", "ರೋಗ ನಿರೋಧಕ ತಳಿಗಳು ಮತ್ತು ಬೆಳೆ ಪರಿವರ್ತನೆ ಬಳಸಿ."]
    },

    "Corn_(maize)___healthy": {
        en: ["Healthy Corn", "Corn", "No visible disease symptoms.", "No medicine required.", "Maintain proper irrigation and nutrition."],
        hi: ["स्वस्थ मक्का", "मक्का", "बीमारी के कोई स्पष्ट लक्षण नहीं।", "किसी दवा की आवश्यकता नहीं है।", "उचित सिंचाई और पोषण बनाए रखें।"],
        kn: ["ಆರೋಗ್ಯಕರ ಮಕ್ಕಿ", "ಮಕ್ಕಿ", "ರೋಗದ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಲಕ್ಷಣಗಳಿಲ್ಲ.", "ಯಾವುದೇ ಔಷಧಿಯ ಅಗತ್ಯವಿಲ್ಲ.", "ಸರಿಯಾದ ನೀರಾವರಿ ಮತ್ತು ಪೋಷಕಾಂಶ ಕಾಪಾಡಿ."]
    },

    "Grape___Black_rot": {
        en: ["Grape Black Rot", "Grape", "Fungal disease affecting grape leaves and fruits.", "Use a registered fungicide according to the product label.", "Remove infected leaves and fruits."],
        hi: ["अंगूर ब्लैक रॉट", "अंगूर", "अंगूर की पत्तियों और फलों का फंगल रोग।", "उत्पाद के लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "संक्रमित पत्तियां और फल हटाएं।"],
        kn: ["ದ್ರಾಕ್ಷಿಯ ಕಪ್ಪು ಕೊಳೆ ರೋಗ", "ದ್ರಾಕ್ಷಿ", "ಎಲೆಗಳು ಮತ್ತು ಹಣ್ಣುಗಳನ್ನು ಬಾಧಿಸುವ ಶಿಲೀಂಧ್ರ ರೋಗ.", "ಉತ್ಪನ್ನದ ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ.", "ಸೋಂಕಿತ ಎಲೆಗಳು ಮತ್ತು ಹಣ್ಣುಗಳನ್ನು ತೆಗೆದುಹಾಕಿ."]
    },

    "Grape___Esca_(Black_Measles)": {
        en: ["Grape Esca Black Measles", "Grape", "Complex fungal disease.", "Remove severely affected material and follow local agricultural recommendations.", "Use healthy planting material."],
        hi: ["अंगूर एस्का ब्लैक मीसल्स", "अंगूर", "जटिल फंगल रोग।", "अधिक प्रभावित भाग हटाएं और स्थानीय कृषि सलाह का पालन करें।", "स्वस्थ पौध सामग्री का उपयोग करें।"],
        kn: ["ದ್ರಾಕ್ಷಿಯ ಎಸ್ಕಾ ಬ್ಲ್ಯಾಕ್ ಮೀಸಲ್ಸ್", "ದ್ರಾಕ್ಷಿ", "ಸಂಕೀರ್ಣ ಶಿಲೀಂಧ್ರ ರೋಗ.", "ಹೆಚ್ಚಾಗಿ ಬಾಧಿತ ಭಾಗಗಳನ್ನು ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಸ್ಥಳೀಯ ಕೃಷಿ ಸಲಹೆ ಅನುಸರಿಸಿ.", "ಆರೋಗ್ಯಕರ ನೆಡುವ ವಸ್ತು ಬಳಸಿ."]
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        en: ["Grape Leaf Blight", "Grape", "Fungal infection affecting grape leaves.", "Use a registered fungicide according to the label.", "Remove fallen leaves and maintain air circulation."],
        hi: ["अंगूर लीफ ब्लाइट", "अंगूर", "पत्तियों को प्रभावित करने वाला फंगल संक्रमण।", "लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "गिरी हुई पत्तियां हटाएं।"],
        kn: ["ದ್ರಾಕ್ಷಿಯ ಎಲೆ ಬ್ಲೈಟ್", "ದ್ರಾಕ್ಷಿ", "ಎಲೆಗಳನ್ನು ಬಾಧಿಸುವ ಶಿಲೀಂಧ್ರ ಸೋಂಕು.", "ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ.", "ಬಿದ್ದ ಎಲೆಗಳನ್ನು ತೆಗೆದುಹಾಕಿ."]
    },

    "Grape___healthy": {
        en: ["Healthy Grape", "Grape", "No visible disease symptoms.", "No medicine required.", "Maintain irrigation, pruning and sanitation."],
        hi: ["स्वस्थ अंगूर", "अंगूर", "बीमारी के कोई स्पष्ट लक्षण नहीं।", "किसी दवा की आवश्यकता नहीं है।", "सिंचाई, छंटाई और स्वच्छता बनाए रखें।"],
        kn: ["ಆರೋಗ್ಯಕರ ದ್ರಾಕ್ಷಿ", "ದ್ರಾಕ್ಷಿ", "ರೋಗದ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಲಕ್ಷಣಗಳಿಲ್ಲ.", "ಯಾವುದೇ ಔಷಧಿಯ ಅಗತ್ಯವಿಲ್ಲ.", "ನೀರಾವರಿ, ಕೊಂಬೆ ಕತ್ತರಿಸುವಿಕೆ ಮತ್ತು ಸ್ವಚ್ಛತೆ ಕಾಪಾಡಿ."]
    },

    "Orange___Haunglongbing_(Citrus_greening)": {
        en: ["Orange Citrus Greening", "Orange", "Disease associated with Candidatus Liberibacter bacteria and insect vectors.", "There is no simple cure. Control insect vectors and follow local agricultural advice.", "Use healthy planting material and control insect vectors."],
        hi: ["संतरा साइट्रस ग्रीनिंग", "संतरा", "बैक्टीरिया और कीट वाहकों से संबंधित रोग।", "इसका सरल उपचार नहीं है। कीट वाहकों को नियंत्रित करें।", "स्वस्थ पौध सामग्री का उपयोग करें।"],
        kn: ["ಕಿತ್ತಳೆ ಸಿಟ್ರಸ್ ಗ್ರೀನಿಂಗ್", "ಕಿತ್ತಳೆ", "ಬ್ಯಾಕ್ಟೀರಿಯಾ ಮತ್ತು ಕೀಟ ವಾಹಕರಿಗೆ ಸಂಬಂಧಿಸಿದ ರೋಗ.", "ಸರಳವಾದ ಗುಣಪಡಿಸುವ ಔಷಧಿಯಿಲ್ಲ. ಕೀಟ ವಾಹಕಗಳನ್ನು ನಿಯಂತ್ರಿಸಿ.", "ಆರೋಗ್ಯಕರ ನೆಡುವ ವಸ್ತು ಬಳಸಿ."]
    },

    "Peach___Bacterial_spot": {
        en: ["Peach Bacterial Spot", "Peach", "Bacterial disease affecting peach leaves and fruits.", "Use a treatment registered for peach bacterial spot according to the label.", "Use healthy planting material and avoid prolonged leaf wetness."],
        hi: ["आड़ू बैक्टीरियल स्पॉट", "आड़ू", "पत्तियों और फलों का बैक्टीरियल रोग।", "लेबल के अनुसार पंजीकृत उपचार का उपयोग करें।", "स्वस्थ पौध सामग्री का उपयोग करें।"],
        kn: ["ಪೀಚ್ ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಸ್ಪಾಟ್", "ಪೀಚ್", "ಎಲೆಗಳು ಮತ್ತು ಹಣ್ಣುಗಳನ್ನು ಬಾಧಿಸುವ ಬ್ಯಾಕ್ಟೀರಿಯಾ ರೋಗ.", "ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಚಿಕಿತ್ಸೆಯನ್ನು ಬಳಸಿ.", "ಆರೋಗ್ಯಕರ ನೆಡುವ ವಸ್ತು ಬಳಸಿ."]
    },

    "Peach___healthy": {
        en: ["Healthy Peach", "Peach", "No visible disease symptoms.", "No medicine required.", "Maintain proper irrigation and nutrition."],
        hi: ["स्वस्थ आड़ू", "आड़ू", "बीमारी के कोई स्पष्ट लक्षण नहीं।", "किसी दवा की आवश्यकता नहीं है।", "उचित सिंचाई और पोषण बनाए रखें।"],
        kn: ["ಆರೋಗ್ಯಕರ ಪೀಚ್", "ಪೀಚ್", "ರೋಗದ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಲಕ್ಷಣಗಳಿಲ್ಲ.", "ಯಾವುದೇ ಔಷಧಿಯ ಅಗತ್ಯವಿಲ್ಲ.", "ಸರಿಯಾದ ನೀರಾವರಿ ಮತ್ತು ಪೋಷಕಾಂಶ ಕಾಪಾಡಿ."]
    },

    "Pepper_Healthy": {
        en: ["Healthy Pepper", "Pepper", "No visible disease symptoms.", "No medicine required.", "Maintain proper irrigation and nutrition."],
        hi: ["स्वस्थ मिर्च", "मिर्च", "बीमारी के कोई स्पष्ट लक्षण नहीं।", "किसी दवा की आवश्यकता नहीं है।", "उचित सिंचाई और पोषण बनाए रखें।"],
        kn: ["ಆರೋಗ್ಯಕರ ಮೆಣಸು", "ಮೆಣಸು", "ರೋಗದ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಲಕ್ಷಣಗಳಿಲ್ಲ.", "ಯಾವುದೇ ಔಷಧಿಯ ಅಗತ್ಯವಿಲ್ಲ.", "ಸರಿಯಾದ ನೀರಾವರಿ ಮತ್ತು ಪೋಷಕಾಂಶ ಕಾಪಾಡಿ."]
    },

    "Potato_Late_Blight": {
        en: ["Potato Late Blight", "Potato", "Phytophthora infestans.", "Metalaxyl-M + Mancozeb or another product registered for potato late blight, according to the product label.", "Use healthy seed and avoid prolonged leaf wetness."],
        hi: ["आलू लेट ब्लाइट", "आलू", "Phytophthora infestans रोगकारक।", "मेटालैक्सिल-एम + मैंकोज़ेब या लेबल के अनुसार पंजीकृत अन्य उत्पाद का उपयोग करें।", "स्वस्थ बीज का उपयोग करें और पत्तियों पर लंबे समय तक नमी से बचें।"],
        kn: ["ಆಲೂಗಡ್ಡೆ ಲೇಟ್ ಬ್ಲೈಟ್", "ಆಲೂಗಡ್ಡೆ", "Phytophthora infestans ರೋಗಕಾರಕ.", "ಮೆಟಾಲಾಕ್ಸಿಲ್-ಎಂ + ಮ್ಯಾಂಕೋಜೆಬ್ ಅಥವಾ ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಉತ್ಪನ್ನ ಬಳಸಿ.", "ಆರೋಗ್ಯಕರ ಬೀಜ ಬಳಸಿ ಮತ್ತು ದೀರ್ಘಕಾಲದ ತೇವಾಂಶ ತಪ್ಪಿಸಿ."]
    },

    "Raspberry___healthy": {
        en: ["Healthy Raspberry", "Raspberry", "No visible disease symptoms.", "No medicine required.", "Maintain proper irrigation and nutrition."],
        hi: ["स्वस्थ रास्पबेरी", "रास्पबेरी", "बीमारी के कोई स्पष्ट लक्षण नहीं।", "किसी दवा की आवश्यकता नहीं है।", "उचित सिंचाई और पोषण बनाए रखें।"],
        kn: ["ಆರೋಗ್ಯಕರ ರಾಸ್ಪ್‌ಬೆರಿ", "ರಾಸ್ಪ್‌ಬೆರಿ", "ರೋಗದ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಲಕ್ಷಣಗಳಿಲ್ಲ.", "ಯಾವುದೇ ಔಷಧಿಯ ಅಗತ್ಯವಿಲ್ಲ.", "ಸರಿಯಾದ ನೀರಾವರಿ ಮತ್ತು ಪೋಷಕಾಂಶ ಕಾಪಾಡಿ."]
    },

    "Soybean___healthy": {
        en: ["Healthy Soybean", "Soybean", "No visible disease symptoms.", "No medicine required.", "Maintain proper irrigation and field monitoring."],
        hi: ["स्वस्थ सोयाबीन", "सोयाबीन", "बीमारी के कोई स्पष्ट लक्षण नहीं।", "किसी दवा की आवश्यकता नहीं है।", "उचित सिंचाई और खेत की निगरानी बनाए रखें।"],
        kn: ["ಆರೋಗ್ಯಕರ ಸೋಯಾಬೀನ್", "ಸೋಯಾಬೀನ್", "ರೋಗದ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಲಕ್ಷಣಗಳಿಲ್ಲ.", "ಯಾವುದೇ ಔಷಧಿಯ ಅಗತ್ಯವಿಲ್ಲ.", "ಸರಿಯಾದ ನೀರಾವರಿ ಮತ್ತು ಹೊಲದ ಮೇಲ್ವಿಚಾರಣೆ ಕಾಪಾಡಿ."]
    },

    "Strawberry___Leaf_scorch": {
        en: ["Strawberry Leaf Scorch", "Strawberry", "Fungal disease causing scorched-looking leaves.", "Use a fungicide registered for strawberry leaf disease according to the label.", "Maintain field sanitation and avoid excessive moisture."],
        hi: ["स्ट्रॉबेरी लीफ स्कॉर्च", "स्ट्रॉबेरी", "पत्तियों को झुलसा हुआ दिखाने वाला फंगल रोग।", "लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "खेत की स्वच्छता बनाए रखें।"],
        kn: ["ಸ್ಟ್ರಾಬೆರಿ ಎಲೆ ಸ್ಕಾರ್ಚ್", "ಸ್ಟ್ರಾಬೆರಿ", "ಎಲೆಗಳು ಸುಟ್ಟಂತೆ ಕಾಣುವ ಶಿಲೀಂಧ್ರ ರೋಗ.", "ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ.", "ಹೊಲದ ಸ್ವಚ್ಛತೆ ಕಾಪಾಡಿ."]
    },

    "Strawberry___healthy": {
        en: ["Healthy Strawberry", "Strawberry", "No visible disease symptoms.", "No medicine required.", "Maintain proper irrigation and nutrition."],
        hi: ["स्वस्थ स्ट्रॉबेरी", "स्ट्रॉबेरी", "बीमारी के कोई स्पष्ट लक्षण नहीं।", "किसी दवा की आवश्यकता नहीं है।", "उचित सिंचाई और पोषण बनाए रखें।"],
        kn: ["ಆರೋಗ್ಯಕರ ಸ್ಟ್ರಾಬೆರಿ", "ಸ್ಟ್ರಾಬೆರಿ", "ರೋಗದ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಲಕ್ಷಣಗಳಿಲ್ಲ.", "ಯಾವುದೇ ಔಷಧಿಯ ಅಗತ್ಯವಿಲ್ಲ.", "ಸರಿಯಾದ ನೀರಾವರಿ ಮತ್ತು ಪೋಷಕಾಂಶ ಕಾಪಾಡಿ."]
    },

    "Tomato_Bacterial_Spot": {
        en: ["Tomato Bacterial Spot", "Tomato", "Bacterial infection.", "Use a treatment registered for tomato bacterial spot according to the label.", "Use clean seed and avoid overhead watering."],
        hi: ["टमाटर बैक्टीरियल स्पॉट", "टमाटर", "बैक्टीरियल संक्रमण।", "लेबल के अनुसार पंजीकृत उपचार का उपयोग करें।", "स्वच्छ बीज का उपयोग करें।"],
        kn: ["ಟೊಮೇಟೊ ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಸ್ಪಾಟ್", "ಟೊಮೇಟೊ", "ಬ್ಯಾಕ್ಟೀರಿಯಾ ಸೋಂಕು.", "ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಚಿಕಿತ್ಸೆಯನ್ನು ಬಳಸಿ.", "ಸ್ವಚ್ಛ ಬೀಜ ಬಳಸಿ."]
    },

    "Tomato_Healthy": {
        en: ["Healthy Tomato", "Tomato", "No visible disease symptoms.", "No medicine required.", "Maintain proper irrigation, nutrition and monitoring."],
        hi: ["स्वस्थ टमाटर", "टमाटर", "बीमारी के कोई स्पष्ट लक्षण नहीं।", "किसी दवा की आवश्यकता नहीं है।", "उचित सिंचाई, पोषण और निगरानी बनाए रखें।"],
        kn: ["ಆರೋಗ್ಯಕರ ಟೊಮೇಟೊ", "ಟೊಮೇಟೊ", "ರೋಗದ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಲಕ್ಷಣಗಳಿಲ್ಲ.", "ಯಾವುದೇ ಔಷಧಿಯ ಅಗತ್ಯವಿಲ್ಲ.", "ಸರಿಯಾದ ನೀರಾವರಿ, ಪೋಷಕಾಂಶ ಮತ್ತು ಪರಿಶೀಲನೆ ಕಾಪಾಡಿ."]
    },

    "Tomato_Late_Blight": {
        en: ["Tomato Late Blight", "Tomato", "Phytophthora infestans.", "Use a fungicide registered for tomato late blight according to the product label.", "Avoid prolonged leaf wetness and maintain air circulation."],
        hi: ["टमाटर लेट ब्लाइट", "टमाटर", "Phytophthora infestans रोगकारक।", "उत्पाद के लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "पत्तियों पर लंबे समय तक नमी से बचें।"],
        kn: ["ಟೊಮೇಟೊ ಲೇಟ್ ಬ್ಲೈಟ್", "ಟೊಮೇಟೊ", "Phytophthora infestans ರೋಗಕಾರಕ.", "ಉತ್ಪನ್ನದ ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕ ಬಳಸಿ.", "ಎಲೆಗಳ ಮೇಲೆ ದೀರ್ಘಕಾಲ ತೇವಾಂಶ ತಪ್ಪಿಸಿ."]
    },

    "Tomato_Septoria_Leaf_Spot": {
        en: ["Tomato Septoria Leaf Spot", "Tomato", "Septoria lycopersici fungus.", "Use a registered fungicide according to the product label.", "Remove infected leaves and avoid overhead watering."],
        hi: ["टमाटर सेप्टोरिया लीफ स्पॉट", "टमाटर", "Septoria lycopersici फंगस।", "उत्पाद के लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "संक्रमित पत्तियां हटाएं।"],
        kn: ["ಟೊಮೇಟೊ ಸೆಪ್ಟೋರಿಯಾ ಎಲೆ ಚುಕ್ಕೆ", "ಟೊಮೇಟೊ", "Septoria lycopersici ಶಿಲೀಂಧ್ರ.", "ಉತ್ಪನ್ನದ ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕ ಬಳಸಿ.", "ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆದುಹಾಕಿ."]
    },

    "Tomato_Target_Spot": {
        en: ["Tomato Target Spot", "Tomato", "Fungal disease affecting tomato leaves and fruits.", "Use a registered fungicide according to the product label.", "Maintain good air circulation and avoid excess moisture."],
        hi: ["टमाटर टारगेट स्पॉट", "टमाटर", "टमाटर की पत्तियों और फलों का फंगल रोग।", "उत्पाद के लेबल के अनुसार पंजीकृत फफूंदनाशी का उपयोग करें।", "अच्छा वायु संचार रखें।"],
        kn: ["ಟೊಮೇಟೊ ಟಾರ್ಗೆಟ್ ಸ್ಪಾಟ್", "ಟೊಮೇಟೊ", "ಎಲೆಗಳು ಮತ್ತು ಹಣ್ಣುಗಳನ್ನು ಬಾಧಿಸುವ ಶಿಲೀಂಧ್ರ ರೋಗ.", "ಉತ್ಪನ್ನದ ಲೇಬಲ್ ಪ್ರಕಾರ ನೋಂದಾಯಿತ ಶಿಲೀಂಧ್ರನಾಶಕ ಬಳಸಿ.", "ಉತ್ತಮ ಗಾಳಿಯ ಸಂಚಾರ ಕಾಪಾಡಿ."]
    },

    "Tomato_Yellow_Leaf_Curl_Virus": {
        en: ["Tomato Yellow Leaf Curl Virus", "Tomato", "Viral disease commonly transmitted by whiteflies.", "There is no direct cure. Control whiteflies and remove severely infected plants.", "Use healthy seedlings and control whiteflies."],
        hi: ["टमाटर येलो लीफ कर्ल वायरस", "टमाटर", "सफेद मक्खी द्वारा फैलने वाला वायरल रोग।", "इसका सीधा उपचार नहीं है। सफेद मक्खी को नियंत्रित करें।", "स्वस्थ पौधों का उपयोग करें।"],
        kn: ["ಟೊಮೇಟೊ ಹಳದಿ ಎಲೆ ಸುರುಳಿ ವೈರಸ್", "ಟೊಮೇಟೊ", "ಬಿಳಿ ಈಚೆಯಿಂದ ಹರಡುವ ವೈರಸ್ ರೋಗ.", "ನೇರ ಗುಣಪಡಿಸುವ ಔಷಧಿಯಿಲ್ಲ. ಬಿಳಿ ಈಚೆಯನ್ನು ನಿಯಂತ್ರಿಸಿ.", "ಆರೋಗ್ಯಕರ ಸಸಿಗಳನ್ನು ಬಳಸಿ."]
    }
};


// ============================================================
// UI TEXT
// ============================================================

const UI = {

    en: {
        selectClass: "-- Select Class --",
        selectImage: "-- Select Test Image --",
        noImage: "No image selected",
        analyze: "Analyze Image",
        cause: "Cause",
        medicine: "Recommended Medicine",
        treatment: "Treatment",
        prevention: "Prevention / Suggestions",
        confidence: "Confidence",
        accuracy: "Model Test Accuracy",
        model: "AI Model",
        plant: "Plant",
        disease: "Disease",
        speak: "Speak Result",
        stop: "Stop Voice",
        camera: "Use Camera",
        closeCamera: "Close Camera",
        capture: "Capture Image"
    },

    hi: {
        selectClass: "-- कक्षा चुनें --",
        selectImage: "-- टेस्ट इमेज चुनें --",
        noImage: "कोई छवि चयनित नहीं है",
        analyze: "छवि का विश्लेषण करें",
        cause: "कारण",
        medicine: "अनुशंसित दवा",
        treatment: "उपचार",
        prevention: "रोकथाम / सुझाव",
        confidence: "विश्वास स्तर",
        accuracy: "मॉडल टेस्ट सटीकता",
        model: "AI मॉडल",
        plant: "पौधा",
        disease: "रोग",
        speak: "परिणाम सुनें",
        stop: "आवाज़ बंद करें",
        camera: "कैमरा उपयोग करें",
        closeCamera: "कैमरा बंद करें",
        capture: "फोटो लें"
    },

    kn: {
        selectClass: "-- ವರ್ಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ --",
        selectImage: "-- ಪರೀಕ್ಷಾ ಚಿತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ --",
        noImage: "ಯಾವುದೇ ಚಿತ್ರ ಆಯ್ಕೆ ಮಾಡಿಲ್ಲ",
        analyze: "ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        cause: "ಕಾರಣ",
        medicine: "ಶಿಫಾರಸು ಮಾಡಿದ ಔಷಧಿ",
        treatment: "ಚಿಕಿತ್ಸೆ",
        prevention: "ತಡೆಗಟ್ಟುವಿಕೆ / ಸಲಹೆಗಳು",
        confidence: "ವಿಶ್ವಾಸ ಮಟ್ಟ",
        accuracy: "ಮಾದರಿ ಪರೀಕ್ಷಾ ನಿಖರತೆ",
        model: "AI ಮಾದರಿ",
        plant: "ಸಸ್ಯ",
        disease: "ರೋಗ",
        speak: "ಫಲಿತಾಂಶವನ್ನು ಕೇಳಿ",
        stop: "ಧ್ವನಿ ನಿಲ್ಲಿಸಿ",
        camera: "ಕ್ಯಾಮೆರಾ ಬಳಸಿ",
        closeCamera: "ಕ್ಯಾಮೆರಾ ಮುಚ್ಚಿ",
        capture: "ಚಿತ್ರ ತೆಗೆದುಕೊಳ್ಳಿ"
    }
};


// ============================================================
// FIND ELEMENT
// ============================================================

function el(...ids) {

    for (const id of ids) {

        const element =
            document.getElementById(id);

        if (element) {
            return element;
        }
    }

    return null;
}


// ============================================================
// SET TEXT
// ============================================================

function setText(ids, value) {

    const element =
        el(...ids);

    if (element) {
        element.textContent =
            value ?? "";
    }
}


// ============================================================
// LOAD CLASSES
// ============================================================

async function loadClasses() {

    const select =
        el(
            "classSelect",
            "diseaseClass",
            "classSelector",
            "plantClass"
        );

    if (!select) {
        return;
    }

    try {

        const response =
            await fetch(
                "/dataset/classes"
            );

        const data =
            await response.json();

        select.innerHTML =
            `<option value="">${UI[selectedLanguage].selectClass}</option>`;

        if (
            !data.classes ||
            !Array.isArray(data.classes)
        ) {
            return;
        }

        data.classes.forEach(
            className => {

                const option =
                    document.createElement(
                        "option"
                    );

                option.value =
                    className;

                option.textContent =
                    getClassDisplayName(
                        className
                    );

                select.appendChild(
                    option
                );
            }
        );

        select.addEventListener(
            "change",
            loadImagesForClass
        );

    } catch (error) {

        console.error(
            "Class loading error:",
            error
        );
    }
}


// ============================================================
// CLASS DISPLAY NAME
// ============================================================

function getClassDisplayName(className) {

    if (INFO[className]) {

        return INFO[className][selectedLanguage][0];
    }

    return className
        .replace(/___/g, " ")
        .replace(/_/g, " ");
}


// ============================================================
// LOAD TEST IMAGES
// ============================================================

async function loadImagesForClass(event) {

    const className =
        event.target.value;

    const imageSelect =
        el(
            "imageSelect",
            "testImageSelect",
            "datasetImage",
            "testImage"
        );

    if (!imageSelect) {
        return;
    }

    imageSelect.innerHTML =
        `<option value="">${UI[selectedLanguage].selectImage}</option>`;

    if (!className) {
        return;
    }

    try {

        const response =
            await fetch(
                "/dataset/images/" +
                encodeURIComponent(className)
            );

        const data =
            await response.json();

        if (
            !data.images ||
            !Array.isArray(data.images)
        ) {
            return;
        }

        data.images.forEach(
            (image, index) => {

                const option =
                    document.createElement(
                        "option"
                    );

                option.value =
                    image.url;

                option.textContent =
                    `Image ${index + 1} - ${image.filename}`;

                imageSelect.appendChild(
                    option
                );
            }
        );

        imageSelect.onchange =
            function () {

                if (this.value) {

                    showDatasetImage(
                        this.value
                    );
                }
            };

    } catch (error) {

        console.error(
            "Image loading error:",
            error
        );
    }
}


// ============================================================
// SHOW DATASET IMAGE
// ============================================================

function showDatasetImage(url) {

    const preview =
        el(
            "imagePreview",
            "previewImage",
            "selectedImage",
            "plantImagePreview"
        );

    if (!preview) {
        return;
    }

    preview.src =
        url;

    preview.style.display =
        "block";

    preview.onload =
        function () {

            const resultArea =
                el(
                    "result",
                    "results",
                    "resultSection"
                );

            if (resultArea) {
                resultArea.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                });
            }
        };
}


// ============================================================
// UPLOAD SETUP
// ============================================================

function setupUpload() {

    const input =
        el(
            "imageInput",
            "fileInput",
            "uploadInput",
            "plantImage"
        );

    const button =
        el(
            "uploadButton",
            "uploadBtn",
            "chooseImageButton"
        );

    if (button && input) {

        button.onclick =
            function () {

                input.click();
            };
    }

    if (input) {

        input.onchange =
            function () {

                const file =
                    this.files[0];

                if (!file) {
                    return;
                }

                selectedFile =
                    file;

                showSelectedFile(
                    file
                );

                showUploadedImage(
                    file
                );

                predictImage(
                    file
                );
            };
    }
}


// ============================================================
// SHOW SELECTED FILE
// ============================================================

function showSelectedFile(file) {

    setText(
        [
            "fileName",
            "selectedFileName"
        ],
        file.name
    );
}


// ============================================================
// SHOW UPLOADED IMAGE
// ============================================================

function showUploadedImage(file) {

    const preview =
        el(
            "imagePreview",
            "previewImage",
            "selectedImage",
            "plantImagePreview"
        );

    if (!preview) {
        return;
    }

    preview.src =
        URL.createObjectURL(
            file
        );

    preview.style.display =
        "block";
}


// ============================================================
// PREDICT IMAGE
// ============================================================

async function predictImage(file) {

    if (!file) {
        return;
    }

    const loading =
        el(
            "loading",
            "loader",
            "loadingMessage"
        );

    if (loading) {

        loading.style.display =
            "block";

        loading.textContent =
            selectedLanguage === "kn"
                ? "ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ..."
                : selectedLanguage === "hi"
                    ? "छवि का विश्लेषण किया जा रहा है..."
                    : "Analyzing image...";
    }

    try {

        const formData =
            new FormData();

        formData.append(
            "image",
            file
        );

        const response =
            await fetch(
                "/predict",
                {
                    method: "POST",
                    body: formData
                }
            );

        const result =
            await response.json();

        if (!response.ok) {

            throw new Error(
                result.message ||
                "Prediction failed"
            );
        }

        currentResult =
            result;

        displayResult(
            result
        );

    } catch (error) {

        console.error(
            error
        );

        alert(
            selectedLanguage === "kn"
                ? "ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ."
                : selectedLanguage === "hi"
                    ? "छवि का विश्लेषण नहीं हो सका।"
                    : "Could not analyze the image."
        );

    } finally {

        if (loading) {
            loading.style.display =
                "none";
        }
    }
}


// ============================================================
// DISPLAY RESULT
// ============================================================

function displayResult(result) {

    const className =
        result.predicted_class ||
        "";

    const info =
        INFO[className];

    let disease;
    let plant;
    let cause;
    let medicine;
    let prevention;

    if (info) {

        const values =
            info[selectedLanguage];

        disease =
            values[0];

        plant =
            values[1];

        cause =
            values[2];

        medicine =
            values[3];

        prevention =
            values[4];

    } else {

        disease =
            result.disease ||
            className;

        plant =
            result.plant ||
            "";

        cause =
            result.cause ||
            "-";

        medicine =
            result.medicine ||
            result.treatment ||
            "-";

        prevention =
            result.prevention ||
            result.suggestions ||
            "-";
    }


    // --------------------------------------------------------
    // CONFIDENCE
    // --------------------------------------------------------

    const confidence =
        Number(
            result.confidence || 0
        ).toFixed(2);


    // --------------------------------------------------------
    // BASIC RESULT
    // --------------------------------------------------------

    setText(
        [
            "diseaseName",
            "disease",
            "predictionDisease",
            "resultDisease"
        ],
        disease
    );

    setText(
        [
            "plantName",
            "plant",
            "predictionPlant",
            "resultPlant"
        ],
        plant
    );

    setText(
        [
            "confidence",
            "confidenceValue",
            "predictionConfidence"
        ],
        confidence + "%"
    );

    setText(
        [
            "testAccuracy",
            "accuracy",
            "modelAccuracy"
        ],
        "96.99%"
    );

    setText(
        [
            "modelName",
            "model"
        ],
        "EfficientNet-B0"
    );

    setText(
        [
            "cause",
            "causeText"
        ],
        cause
    );

    setText(
        [
            "medicine",
            "medicineText",
            "recommendedMedicine",
            "medicineRecommendation"
        ],
        medicine
    );

    setText(
        [
            "treatment",
            "treatmentText"
        ],
        medicine
    );

    setText(
        [
            "prevention",
            "preventionText",
            "suggestions"
        ],
        prevention
    );


    // --------------------------------------------------------
    // SHOW RESULT AREA
    // --------------------------------------------------------

    const resultArea =
        el(
            "result",
            "results",
            "resultSection"
        );

    if (resultArea) {

        resultArea.style.display =
            "block";

        resultArea.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }


    // --------------------------------------------------------
    // CONFIDENCE LEVEL
    // --------------------------------------------------------

    let confidenceText;

    if (confidence >= 70) {

        confidenceText =
            selectedLanguage === "kn"
                ? "ಹೆಚ್ಚಿನ ವಿಶ್ವಾಸ"
                : selectedLanguage === "hi"
                    ? "उच्च विश्वास"
                    : "High Confidence";

    } else if (confidence >= 50) {

        confidenceText =
            selectedLanguage === "kn"
                ? "ಮಧ್ಯಮ ವಿಶ್ವಾಸ"
                : selectedLanguage === "hi"
                    ? "मध्यम विश्वास"
                    : "Moderate Confidence";

    } else {

        confidenceText =
            selectedLanguage === "kn"
                ? "ಕಡಿಮೆ ವಿಶ್ವಾಸ"
                : selectedLanguage === "hi"
                    ? "कम विश्वास"
                    : "Low Confidence";
    }

    setText(
        [
            "confidenceLevel"
        ],
        confidenceText
    );


    // --------------------------------------------------------
    // VOICE BUTTON
    // --------------------------------------------------------

    const speakButton =
        el(
            "speakButton",
            "speakBtn",
            "voiceButton"
        );

    if (speakButton) {

        speakButton.style.display =
            "inline-block";

        speakButton.onclick =
            function () {

                speakResult();
            };
    }
}


// ============================================================
// SPEAK RESULT USING BACKEND EDGE TTS
// ============================================================

async function speakResult() {

    if (!currentResult) {
        return;
    }

    const className =
        currentResult.predicted_class;

    const info =
        INFO[className];

    let text = "";

    if (info) {

        const values =
            info[selectedLanguage];

        text =
            `${UI[selectedLanguage].plant}: ${values[1]}. ` +
            `${UI[selectedLanguage].disease}: ${values[0]}. ` +
            `${UI[selectedLanguage].confidence}: ${Number(currentResult.confidence || 0).toFixed(2)} percent. ` +
            `${UI[selectedLanguage].cause}: ${values[2]}. ` +
            `${UI[selectedLanguage].medicine}: ${values[3]}. ` +
            `${UI[selectedLanguage].prevention}: ${values[4]}.`;

    } else {

        text =
            currentResult.disease ||
            currentResult.predicted_class ||
            "";
    }

    try {

        const formData =
            new FormData();

        formData.append(
            "text",
            text
        );

        formData.append(
            "language",
            selectedLanguage
        );

        const response =
            await fetch(
                "/tts",
                {
                    method: "POST",
                    body: formData
                }
            );

        if (!response.ok) {
            throw new Error(
                "TTS failed"
            );
        }

        const blob =
            await response.blob();

        const audioURL =
            URL.createObjectURL(
                blob
            );

        const audio =
            new Audio(
                audioURL
            );

        audio.play();

    } catch (error) {

        console.error(
            "TTS error:",
            error
        );

        // Browser fallback

        if (
            "speechSynthesis"
            in window
        ) {

            const speech =
                new SpeechSynthesisUtterance(
                    text
                );

            speech.lang =
                selectedLanguage === "kn"
                    ? "kn-IN"
                    : selectedLanguage === "hi"
                        ? "hi-IN"
                        : "en-IN";

            speechSynthesis.cancel();

            speechSynthesis.speak(
                speech
            );
        }
    }
}


// ============================================================
// LANGUAGE CHANGE
// ============================================================

function setupLanguage() {

    const languageSelect =
        el(
            "languageSelect",
            "language",
            "langSelect"
        );

    if (!languageSelect) {
        return;
    }

    languageSelect.onchange =
        function () {

            selectedLanguage =
                this.value;

            if (
                !["en", "hi", "kn"].includes(
                    selectedLanguage
                )
            ) {

                selectedLanguage =
                    "en";
            }

            updateUILanguage();

            reloadClassNames();

            if (currentResult) {

                displayResult(
                    currentResult
                );
            }
        };
}


// ============================================================
// UPDATE UI LANGUAGE
// ============================================================

function updateUILanguage() {

    const language =
        UI[selectedLanguage];


    setText(
        ["causeTitle"],
        language.cause
    );

    setText(
        ["medicineTitle"],
        language.medicine
    );

    setText(
        ["treatmentTitle"],
        language.treatment
    );

    setText(
        ["preventionTitle"],
        language.prevention
    );

    setText(
        ["confidenceTitle"],
        language.confidence
    );

    setText(
        ["accuracyTitle"],
        language.accuracy
    );

    setText(
        ["modelTitle"],
        language.model
    );

    setText(
        ["plantTitle"],
        language.plant
    );

    setText(
        ["diseaseTitle"],
        language.disease
    );

    setText(
        ["speakButton"],
        "🔊 " + language.speak
    );

    setText(
        ["cameraButton"],
        "📷 " + language.camera
    );

    setText(
        ["captureButton"],
        "📸 " + language.capture
    );
}


// ============================================================
// RELOAD CLASS DISPLAY NAMES
// ============================================================

function reloadClassNames() {

    const select =
        el(
            "classSelect",
            "diseaseClass",
            "classSelector",
            "plantClass"
        );

    if (!select) {
        return;
    }

    Array.from(
        select.options
    ).forEach(
        option => {

            if (
                option.value
            ) {

                option.textContent =
                    getClassDisplayName(
                        option.value
                    );
            }
        }
    );
}


// ============================================================
// CAMERA
// ============================================================

function setupCamera() {

    const cameraButton =
        el(
            "cameraButton",
            "cameraBtn",
            "useCamera"
        );

    const captureButton =
        el(
            "captureButton",
            "captureBtn"
        );

    const video =
        el(
            "cameraVideo",
            "video"
        );

    const canvas =
        el(
            "cameraCanvas",
            "canvas"
        );

    if (
        cameraButton &&
        video
    ) {

        cameraButton.onclick =
            async function () {

                try {

                    cameraStream =
                        await navigator.mediaDevices.getUserMedia(
                            {
                                video: true
                            }
                        );

                    video.srcObject =
                        cameraStream;

                    video.style.display =
                        "block";

                    if (captureButton) {

                        captureButton.style.display =
                            "inline-block";
                    }

                } catch (error) {

                    console.error(
                        error
                    );

                    alert(
                        "Camera access was not available."
                    );
                }
            };
    }

    if (
        captureButton &&
        video &&
        canvas
    ) {

        captureButton.onclick =
            function () {

                const context =
                    canvas.getContext(
                        "2d"
                    );

                canvas.width =
                    video.videoWidth;

                canvas.height =
                    video.videoHeight;

                context.drawImage(
                    video,
                    0,
                    0,
                    canvas.width,
                    canvas.height
                );

                canvas.toBlob(
                    function (blob) {

                        if (!blob) {
                            return;
                        }

                        selectedFile =
                            new File(
                                [blob],
                                "camera_plant.jpg",
                                {
                                    type: "image/jpeg"
                                }
                            );

                        showSelectedFile(
                            selectedFile
                        );

                        showUploadedImage(
                            selectedFile
                        );

                        predictImage(
                            selectedFile
                        );

                    },
                    "image/jpeg",
                    0.95
                );
            };
    }
}


// ============================================================
// RANDOM IMAGE
// ============================================================

function setupRandomImage() {

    const randomButton =
        el(
            "randomButton",
            "randomBtn",
            "selectRandomImage"
        );

    if (!randomButton) {
        return;
    }

    randomButton.onclick =
        async function () {

            const classSelect =
                el(
                    "classSelect",
                    "diseaseClass",
                    "classSelector",
                    "plantClass"
                );

            if (!classSelect) {
                return;
            }

            const options =
                Array.from(
                    classSelect.options
                ).filter(
                    option =>
                        option.value
                );

            if (options.length === 0) {
                return;
            }

            const randomOption =
                options[
                    Math.floor(
                        Math.random() *
                        options.length
                    )
                ];

            classSelect.value =
                randomOption.value;

            classSelect.dispatchEvent(
                new Event(
                    "change"
                )
            );

            setTimeout(
                function () {

                    const imageSelect =
                        el(
                            "imageSelect",
                            "testImageSelect",
                            "datasetImage",
                            "testImage"
                        );

                    if (
                        !imageSelect ||
                        imageSelect.options.length <= 1
                    ) {
                        return;
                    }

                    const imageOptions =
                        Array.from(
                            imageSelect.options
                        ).filter(
                            option =>
                                option.value
                        );

                    const randomImage =
                        imageOptions[
                            Math.floor(
                                Math.random() *
                                imageOptions.length
                            )
                        ];

                    imageSelect.value =
                        randomImage.value;

                    showDatasetImage(
                        randomImage.value
                    );

                },
                500
            );
        };
}


// ============================================================
// INITIALIZE
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "PlantCare AI frontend started."
        );

        setupUpload();

        setupLanguage();

        setupCamera();

        setupRandomImage();

        loadClasses();

        updateUILanguage();
    }
);