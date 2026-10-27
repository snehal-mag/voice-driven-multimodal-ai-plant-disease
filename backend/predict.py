# ============================================================
# PLANTCARE AI - 38 CLASS PREDICTION + 5 POINT ADVISORY SYSTEM
# ============================================================

import json
from pathlib import Path

import torch
from PIL import Image
from torchvision import models, transforms


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"

MODEL_PATH = MODEL_DIR / "expanded_38_model_best.pth"
CLASSES_PATH = MODEL_DIR / "expanded_38_classes.json"
RESULTS_PATH = MODEL_DIR / "expanded_38_test_results.json"


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ============================================================
# LOAD CLASS LABELS
# ============================================================

with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    CLASSES = json.load(f)

NUM_CLASSES = len(CLASSES)

if NUM_CLASSES != 38:
    raise ValueError(
        f"Expected 38 classes, but found {NUM_CLASSES}."
    )


# ============================================================
# IMAGE TRANSFORMATION
# ============================================================

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ============================================================
# LOAD EFFICIENTNET-B0
# ============================================================

model = models.efficientnet_b0(weights=None)

in_features = model.classifier[1].in_features

model.classifier = torch.nn.Sequential(
    torch.nn.Dropout(0.3),
    torch.nn.Linear(in_features, NUM_CLASSES)
)

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE,
    weights_only=True
)

if isinstance(checkpoint, dict) and "state_dict" in checkpoint:
    model.load_state_dict(checkpoint["state_dict"])
else:
    model.load_state_dict(checkpoint)

model.to(DEVICE)
model.eval()


# ============================================================
# TEST ACCURACY
# ============================================================

TEST_ACCURACY = 94.91

try:
    if RESULTS_PATH.exists():
        with open(RESULTS_PATH, "r", encoding="utf-8") as f:
            results = json.load(f)

        if "test_accuracy" in results:
            TEST_ACCURACY = float(results["test_accuracy"])
        elif "accuracy" in results:
            TEST_ACCURACY = float(results["accuracy"])

except (OSError, ValueError, TypeError, json.JSONDecodeError):
    TEST_ACCURACY = 94.91


# ============================================================
# DISEASE INFORMATION
# ============================================================

DISEASE_INFO = {
    "Apple___Apple_scab": {
        "plant": "Apple",
        "disease": "Apple Scab",
        "causes": [
            "Caused mainly by the fungus Venturia inaequalis.",
            "Wet leaves and humid conditions favor infection.",
            "Rain splash and air movement can spread fungal spores.",
            "Infected fallen leaves can produce new spores.",
            "Young leaves and developing fruit are susceptible."
        ],
        "medicine": [
            "Remove severely infected leaves and fruit where practical.",
            "Improve canopy airflow through appropriate pruning.",
            "Use a locally registered apple-scab fungicide when recommended.",
            "Rotate fungicide modes of action to reduce resistance risk.",
            "Follow the product label and local agricultural advice."
        ],
        "prevention": [
            "Use resistant apple varieties where available.",
            "Remove or manage infected fallen leaves.",
            "Maintain good air circulation inside the canopy.",
            "Avoid unnecessarily prolonged leaf wetness.",
            "Inspect new leaves regularly."
        ]
    },

    "Apple___Black_rot": {
        "plant": "Apple",
        "disease": "Apple Black Rot",
        "causes": [
            "Commonly associated with the fungus Botryosphaeria obtusa.",
            "Dead wood can provide a source of infection.",
            "Mummified fruit can carry fungal inoculum.",
            "Wounds can provide entry points for the pathogen.",
            "Warm and wet conditions can increase disease development."
        ],
        "medicine": [
            "Prune and remove severely infected branches.",
            "Remove mummified fruit from trees and the orchard floor.",
            "Disinfect pruning tools when practical.",
            "Use a locally registered fungicide when recommended.",
            "Follow the product label and local agricultural advice."
        ],
        "prevention": [
            "Maintain good orchard sanitation.",
            "Remove dead branches regularly.",
            "Avoid unnecessary wounds during pruning.",
            "Maintain good canopy ventilation.",
            "Inspect branches and fruit regularly."
        ]
    },

    "Apple___Cedar_apple_rust": {
        "plant": "Apple",
        "disease": "Apple Cedar Apple Rust",
        "causes": [
            "Caused by the fungus Gymnosporangium juniperi-virginianae.",
            "The pathogen alternates between apple and juniper hosts.",
            "Spores can spread during wet spring weather.",
            "Young leaves and fruit may be affected.",
            "Nearby susceptible junipers can contribute to disease cycles."
        ],
        "medicine": [
            "Confirm the disease before considering treatment.",
            "Use a locally registered product when recommended.",
            "Apply treatments at the crop-specific recommended growth stage.",
            "Follow the product label.",
            "Consult a local horticultural specialist for severe cases."
        ],
        "prevention": [
            "Choose resistant apple varieties where available.",
            "Inspect leaves for orange rust spots.",
            "Manage nearby host plants where practical and appropriate.",
            "Maintain orchard health.",
            "Monitor trees during spring."
        ]
    },

    "Apple___healthy": {
        "plant": "Apple",
        "disease": "Healthy",
        "causes": [
            "No visible disease pattern was detected by the model.",
            "The image matches the healthy apple class.",
            "No obvious leaf disease pattern was identified.",
            "The plant appears visually healthy.",
            "Hidden stress may still exist without visible symptoms."
        ],
        "medicine": [
            "No disease medicine is indicated by this prediction.",
            "Avoid unnecessary pesticide applications.",
            "Maintain balanced nutrition.",
            "Maintain suitable irrigation.",
            "Consult an expert if symptoms develop."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Maintain orchard sanitation.",
            "Monitor leaves and fruit regularly.",
            "Maintain good canopy airflow.",
            "Continue routine plant care."
        ]
    },

    "Blueberry___healthy": {
        "plant": "Blueberry",
        "disease": "Healthy",
        "causes": [
            "No visible disease pattern was detected by the model.",
            "The image matches the healthy blueberry class.",
            "No obvious leaf disease pattern was identified.",
            "The plant appears visually healthy.",
            "Environmental stress may exist without visible symptoms."
        ],
        "medicine": [
            "No disease medicine is indicated by this prediction.",
            "Avoid unnecessary pesticide applications.",
            "Maintain suitable soil acidity for blueberries.",
            "Maintain appropriate irrigation.",
            "Seek expert advice if symptoms develop."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Monitor leaves and stems regularly.",
            "Maintain suitable soil conditions.",
            "Provide appropriate sunlight and irrigation.",
            "Maintain garden or field sanitation."
        ]
    },

    "Cherry_(including_sour)___Powdery_mildew": {
        "plant": "Cherry",
        "disease": "Cherry Powdery Mildew",
        "causes": [
            "Caused by powdery mildew fungi.",
            "Susceptible young leaves can develop white fungal growth.",
            "The disease can spread between plants.",
            "Dense growth may reduce airflow.",
            "Weather conditions influence disease development."
        ],
        "medicine": [
            "Remove severely affected material where practical.",
            "Improve airflow through suitable pruning.",
            "Use a locally registered product when recommended.",
            "Rotate product modes of action where applicable.",
            "Follow the crop-specific label."
        ],
        "prevention": [
            "Maintain appropriate spacing and airflow.",
            "Inspect young leaves regularly.",
            "Avoid excessive nitrogen application.",
            "Remove heavily infected material when practical.",
            "Use tolerant varieties where available."
        ]
    },

    "Cherry_(including_sour)___healthy": {
        "plant": "Cherry",
        "disease": "Healthy",
        "causes": [
            "No visible disease pattern was detected by the model.",
            "The image matches the healthy cherry class.",
            "No obvious leaf disease pattern was identified.",
            "The plant appears visually healthy.",
            "Continue monitoring for emerging symptoms."
        ],
        "medicine": [
            "No disease medicine is indicated by this prediction.",
            "Avoid unnecessary pesticide applications.",
            "Maintain balanced nutrition.",
            "Water according to plant needs.",
            "Seek expert advice if symptoms appear."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Maintain orchard sanitation.",
            "Monitor leaves and fruit.",
            "Maintain good canopy airflow.",
            "Prune appropriately for the variety."
        ]
    },

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "plant": "Corn",
        "disease": "Corn Cercospora Leaf Spot / Gray Leaf Spot",
        "causes": [
            "Associated with Cercospora species causing gray leaf spot.",
            "Warm and humid conditions favor disease development.",
            "Wind and rain can spread spores.",
            "Infected crop residue can carry the pathogen.",
            "Dense crop canopies can maintain high humidity."
        ],
        "medicine": [
            "Use a locally registered corn fungicide when treatment is justified.",
            "Apply fungicide according to the crop-specific label.",
            "Rotate fungicide modes of action to reduce resistance risk.",
            "Manage infected crop residue where appropriate.",
            "Consult local agricultural guidance for application timing."
        ],
        "prevention": [
            "Use resistant or tolerant hybrids.",
            "Practice crop rotation where appropriate.",
            "Manage infected crop residue.",
            "Scout fields regularly.",
            "Avoid unnecessary prolonged leaf wetness."
        ]
    },

    "Corn_(maize)___Common_rust_": {
        "plant": "Corn",
        "disease": "Corn Common Rust",
        "causes": [
            "Caused by rust fungi such as Puccinia species.",
            "Wind can carry rust spores over long distances.",
            "Moist leaf surfaces support infection.",
            "Cool to moderate conditions can favor disease development.",
            "Susceptible hybrids can show more severe symptoms."
        ],
        "medicine": [
            "Monitor disease severity before chemical treatment.",
            "Use a locally registered corn fungicide when justified.",
            "Select a registered active ingredient according to local guidance.",
            "Rotate fungicide modes of action when repeated treatment is required.",
            "Follow label requirements and harvest restrictions."
        ],
        "prevention": [
            "Use resistant or tolerant corn hybrids.",
            "Scout fields regularly.",
            "Remove volunteer corn where practical.",
            "Maintain balanced crop nutrition.",
            "Monitor weather conditions favorable to rust."
        ]
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "plant": "Corn",
        "disease": "Corn Northern Leaf Blight",
        "causes": [
            "Caused by Exserohilum turcicum.",
            "The pathogen can survive in infected crop residue.",
            "Wind and rain help spread spores.",
            "Cool and humid conditions can favor development.",
            "Susceptible corn hybrids can develop large leaf lesions."
        ],
        "medicine": [
            "Use a locally registered fungicide when disease pressure is significant.",
            "Apply treatment according to the crop-specific label.",
            "Rotate fungicide modes of action.",
            "Manage infected crop residue.",
            "Consult local agricultural experts for treatment timing."
        ],
        "prevention": [
            "Plant tolerant or resistant hybrids.",
            "Practice crop rotation where appropriate.",
            "Manage infected residue.",
            "Scout lower leaves early.",
            "Avoid prolonged leaf wetness where possible."
        ]
    },

    "Corn_(maize)___healthy": {
        "plant": "Corn",
        "disease": "Healthy",
        "causes": [
            "No visible disease symptoms were detected.",
            "The image matches the healthy corn class.",
            "No obvious leaf disease pattern was identified.",
            "The plant appears visually healthy.",
            "Environmental stress may still exist without visible symptoms."
        ],
        "medicine": [
            "No disease medicine is indicated.",
            "Avoid unnecessary pesticide applications.",
            "Maintain balanced crop nutrition.",
            "Maintain suitable soil moisture.",
            "Continue regular field monitoring."
        ],
        "prevention": [
            "Use healthy seed.",
            "Use suitable crop rotation.",
            "Monitor plants regularly.",
            "Maintain balanced nutrition.",
            "Manage weeds and crop residue appropriately."
        ]
    },

    "Grape___Black_rot": {
        "plant": "Grape",
        "disease": "Grape Black Rot",
        "causes": [
            "Caused by the fungus Guignardia bidwellii.",
            "Infected berries and plant debris can produce spores.",
            "Rain can spread spores to healthy plant tissue.",
            "Warm and wet weather favors disease development.",
            "Poor sanitation can increase disease pressure."
        ],
        "medicine": [
            "Remove infected berries and mummified fruit.",
            "Prune severely infected tissue where appropriate.",
            "Use a locally registered grape fungicide when recommended.",
            "Rotate fungicide modes of action to reduce resistance risk.",
            "Follow the grape-specific product label."
        ],
        "prevention": [
            "Maintain vineyard sanitation.",
            "Remove mummified berries.",
            "Improve canopy airflow.",
            "Avoid excessive canopy density.",
            "Scout vines regularly."
        ]
    },

    "Grape___Esca_(Black_Measles)": {
        "plant": "Grape",
        "disease": "Grape Esca / Black Measles",
        "causes": [
            "Associated with several wood-decay fungi.",
            "Fungi can enter through pruning wounds.",
            "Infected woody tissue can remain a disease source.",
            "Plant stress can contribute to disease severity.",
            "Poor pruning-wound management can increase risk."
        ],
        "medicine": [
            "Remove severely affected wood where practical.",
            "Prune during appropriate dry conditions.",
            "Avoid creating unnecessary large pruning wounds.",
            "There is no simple curative fungicide for established wood disease.",
            "Consult a local grape-production specialist for severe cases."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Use careful pruning practices.",
            "Protect important pruning wounds where locally recommended.",
            "Remove infected wood from the vineyard.",
            "Maintain overall vine health."
        ]
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "plant": "Grape",
        "disease": "Grape Leaf Blight",
        "causes": [
            "Associated with fungal leaf-spot pathogens.",
            "High humidity can favor disease development.",
            "Rain splash can move spores between leaves.",
            "Dense canopies can retain moisture.",
            "Infected leaves can contribute to disease spread."
        ],
        "medicine": [
            "Remove heavily infected leaves where practical.",
            "Improve vineyard airflow.",
            "Use a locally registered fungicide when recommended.",
            "Rotate fungicide modes of action.",
            "Follow the crop-specific product label."
        ],
        "prevention": [
            "Maintain good canopy management.",
            "Remove infected leaves when practical.",
            "Avoid unnecessary prolonged leaf wetness.",
            "Monitor vines regularly.",
            "Maintain vineyard sanitation."
        ]
    },

    "Grape___healthy": {
        "plant": "Grape",
        "disease": "Healthy",
        "causes": [
            "No visible disease symptoms were detected.",
            "The image matches the healthy grape class.",
            "No obvious leaf disease pattern was identified.",
            "The plant appears visually healthy.",
            "Regular monitoring is still recommended."
        ],
        "medicine": [
            "No disease medicine is indicated.",
            "Avoid unnecessary pesticide application.",
            "Maintain normal vine nutrition.",
            "Maintain suitable irrigation.",
            "Consult an expert if new symptoms develop."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Maintain vineyard sanitation.",
            "Monitor leaves and fruit.",
            "Maintain canopy airflow.",
            "Remove severely damaged plant material when appropriate."
        ]
    },

    "Orange___Haunglongbing_(Citrus_greening)": {
        "plant": "Orange",
        "disease": "Citrus Greening / Huanglongbing",
        "causes": [
            "Associated with Candidatus Liberibacter bacteria.",
            "The disease is mainly spread by citrus psyllid insect vectors.",
            "Infected planting material can spread the pathogen.",
            "Infected trees can act as sources of infection.",
            "The disease can cause leaf mottling and tree decline."
        ],
        "medicine": [
            "There is no curative medicine that eliminates HLB from an infected tree.",
            "Manage citrus psyllids using locally registered products when recommended.",
            "Rotate insecticide modes of action according to local guidance.",
            "Remove infected trees where local authorities recommend removal.",
            "Follow local pesticide labels and disease-management recommendations."
        ],
        "prevention": [
            "Use certified healthy planting material.",
            "Monitor new plant growth for psyllids.",
            "Inspect trees regularly for symptoms.",
            "Control psyllids according to local recommendations.",
            "Follow applicable quarantine and plant-movement requirements."
        ]
    },

    "Peach___Bacterial_spot": {
        "plant": "Peach",
        "disease": "Peach Bacterial Spot",
        "causes": [
            "Caused by bacterial pathogens such as Xanthomonas species.",
            "Rain and water splash can spread bacteria.",
            "Wounds can provide infection sites.",
            "Warm and wet conditions favor disease development.",
            "Susceptible cultivars can show greater disease severity."
        ],
        "medicine": [
            "Remove severely damaged plant material where practical.",
            "Use locally registered copper-based products when recommended.",
            "Some regions may permit other registered bacterial-disease products.",
            "Avoid excessive repeated copper applications.",
            "Follow the peach-specific product label and local guidance."
        ],
        "prevention": [
            "Use tolerant varieties where available.",
            "Maintain good orchard airflow.",
            "Avoid unnecessary overhead irrigation.",
            "Remove severely infected material.",
            "Monitor new leaves and fruit regularly."
        ]
    },

    "Peach___healthy": {
        "plant": "Peach",
        "disease": "Healthy",
        "causes": [
            "No visible disease symptoms were detected.",
            "The image matches the healthy peach class.",
            "No obvious leaf disease pattern was identified.",
            "The plant appears visually healthy.",
            "Continued monitoring is recommended."
        ],
        "medicine": [
            "No disease medicine is indicated.",
            "Avoid unnecessary fungicide or bactericide application.",
            "Maintain normal nutrition.",
            "Maintain appropriate irrigation.",
            "Seek expert diagnosis if symptoms appear."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Maintain orchard sanitation.",
            "Monitor leaves and fruit.",
            "Maintain good canopy airflow.",
            "Remove damaged plant material when appropriate."
        ]
    },

    "Pepper_Bacterial_Spot": {
        "plant": "Pepper",
        "disease": "Bacterial Spot",
        "causes": [
            "Associated with bacterial pathogens such as Xanthomonas species.",
            "Rain and water splash can spread bacteria.",
            "Contaminated seed or seedlings can introduce infection.",
            "Warm and wet conditions can favor disease development.",
            "Handling wet plants can contribute to spread."
        ],
        "medicine": [
            "Remove severely infected plant material where practical.",
            "Use locally registered products only when recommended.",
            "Copper products may be used where locally permitted.",
            "Avoid repeated unnecessary chemical applications.",
            "Follow product labels and local agricultural guidance."
        ],
        "prevention": [
            "Use healthy seed and seedlings.",
            "Avoid unnecessary overhead irrigation.",
            "Sanitize tools where practical.",
            "Maintain suitable plant spacing.",
            "Remove infected crop debris appropriately."
        ]
    },

    "Pepper_Healthy": {
        "plant": "Pepper",
        "disease": "Healthy",
        "causes": [
            "No visible disease symptoms were detected.",
            "The image matches the healthy pepper class.",
            "No obvious disease pattern was identified.",
            "The plant appears visually healthy.",
            "Hidden stress may still exist without visible symptoms."
        ],
        "medicine": [
            "No disease medicine is indicated.",
            "Avoid unnecessary pesticide application.",
            "Maintain balanced crop nutrition.",
            "Maintain proper irrigation.",
            "Consult an agricultural expert if symptoms develop."
        ],
        "prevention": [
            "Use healthy seed and planting material.",
            "Maintain field sanitation.",
            "Monitor leaves regularly.",
            "Control weeds and pests appropriately.",
            "Maintain suitable irrigation and nutrition."
        ]
    },

    "Potato_Early_Blight": {
        "plant": "Potato",
        "disease": "Early Blight",
        "causes": [
            "Commonly associated with Alternaria species.",
            "Older leaves may show brown lesions with concentric rings.",
            "Plant stress can increase disease severity.",
            "Spores can spread through wind and rain.",
            "Warm conditions and leaf wetness can favor disease."
        ],
        "medicine": [
            "Remove severely affected leaves where practical.",
            "Use a locally registered potato fungicide when recommended.",
            "Rotate fungicide modes of action where applicable.",
            "Avoid unnecessary chemical applications.",
            "Follow product labels and local agricultural guidance."
        ],
        "prevention": [
            "Use healthy seed potatoes.",
            "Maintain balanced plant nutrition.",
            "Avoid prolonged leaf wetness.",
            "Remove infected crop debris where appropriate.",
            "Scout lower leaves regularly."
        ]
    },

    "Potato_Healthy": {
        "plant": "Potato",
        "disease": "Healthy",
        "causes": [
            "No visible disease pattern was detected by the model.",
            "The image matches the healthy potato class.",
            "No obvious leaf disease pattern was identified.",
            "The plant appears visually healthy.",
            "Continue field monitoring."
        ],
        "medicine": [
            "No disease medicine is indicated by this prediction.",
            "Avoid unnecessary pesticide applications.",
            "Maintain balanced nutrition.",
            "Water according to crop needs.",
            "Seek expert advice if symptoms develop."
        ],
        "prevention": [
            "Use healthy seed tubers.",
            "Monitor leaves regularly.",
            "Maintain suitable soil moisture.",
            "Manage weeds appropriately.",
            "Practice suitable crop rotation."
        ]
    },

    "Potato_Late_Blight": {
        "plant": "Potato",
        "disease": "Late Blight",
        "causes": [
            "Caused by the oomycete Phytophthora infestans.",
            "Cool and wet conditions can strongly favor disease development.",
            "Spores can spread through wind and rain.",
            "Infected plant debris or tubers can carry inoculum.",
            "Rapid disease development can occur under favorable weather."
        ],
        "medicine": [
            "Use a locally registered late-blight fungicide when recommended.",
            "Protectant fungicides may be part of an integrated program.",
            "Rotate fungicide modes of action to reduce resistance risk.",
            "Manage severely infected plant material appropriately.",
            "Follow product labels and local agricultural guidance."
        ],
        "prevention": [
            "Use certified disease-free seed tubers.",
            "Scout fields frequently.",
            "Avoid excessive leaf wetness where possible.",
            "Destroy volunteer potatoes where appropriate.",
            "Follow local late-blight management recommendations."
        ]
    },

    "Raspberry___healthy": {
        "plant": "Raspberry",
        "disease": "Healthy",
        "causes": [
            "No visible disease symptoms were detected.",
            "The image matches the healthy raspberry class.",
            "No obvious leaf disease pattern was identified.",
            "The plant appears visually healthy.",
            "Regular monitoring remains important."
        ],
        "medicine": [
            "No disease medicine is indicated.",
            "Avoid unnecessary pesticide application.",
            "Maintain normal crop nutrition.",
            "Maintain suitable irrigation.",
            "Consult an expert if symptoms develop."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Maintain good field sanitation.",
            "Monitor leaves and fruit regularly.",
            "Maintain good airflow.",
            "Remove damaged plant material when appropriate."
        ]
    },

    "Soybean___healthy": {
        "plant": "Soybean",
        "disease": "Healthy",
        "causes": [
            "No visible disease symptoms were detected.",
            "The image matches the healthy soybean class.",
            "No obvious disease lesion was identified.",
            "The plant appears visually healthy.",
            "Continued field scouting is recommended."
        ],
        "medicine": [
            "No disease medicine is indicated.",
            "Avoid unnecessary fungicide applications.",
            "Maintain balanced crop nutrition.",
            "Maintain appropriate soil moisture.",
            "Seek expert diagnosis if symptoms develop."
        ],
        "prevention": [
            "Use healthy seed.",
            "Practice suitable crop rotation.",
            "Monitor plants regularly.",
            "Maintain balanced nutrition.",
            "Manage weeds and crop residue appropriately."
        ]
    },

    "Squash_Powdery_Mildew": {
        "plant": "Squash",
        "disease": "Powdery Mildew",
        "causes": [
            "Caused by powdery mildew fungi.",
            "White powdery patches can develop on leaves.",
            "Susceptible plants are more likely to become infected.",
            "Dense foliage can reduce airflow.",
            "Disease development depends on local environmental conditions."
        ],
        "medicine": [
            "Remove severely affected leaves where practical.",
            "Use a locally registered product when recommended.",
            "Rotate product modes of action where applicable.",
            "Avoid unnecessary chemical applications.",
            "Follow crop-specific product labels."
        ],
        "prevention": [
            "Use tolerant varieties where available.",
            "Provide suitable plant spacing.",
            "Improve airflow around foliage.",
            "Monitor leaves regularly.",
            "Remove infected plant debris appropriately."
        ]
    },

    "Strawberry___Leaf_scorch": {
        "plant": "Strawberry",
        "disease": "Leaf Scorch",
        "causes": [
            "Associated with fungal leaf-spot pathogens.",
            "Wet foliage can favor disease development.",
            "Rain splash can spread spores.",
            "Dense plant growth can increase humidity.",
            "Infected leaves can provide a source of inoculum."
        ],
        "medicine": [
            "Remove severely infected leaves where practical.",
            "Improve airflow around plants.",
            "Use a locally registered fungicide when recommended.",
            "Rotate fungicide modes of action where required.",
            "Follow the strawberry-specific product label."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Remove heavily infected leaves.",
            "Avoid prolonged leaf wetness.",
            "Maintain suitable plant spacing.",
            "Scout plants regularly."
        ]
    },

    "Strawberry___healthy": {
        "plant": "Strawberry",
        "disease": "Healthy",
        "causes": [
            "No visible disease symptoms were detected.",
            "The image matches the healthy strawberry class.",
            "No obvious leaf disease pattern was identified.",
            "The plant appears visually healthy.",
            "Continued monitoring is recommended."
        ],
        "medicine": [
            "No disease medicine is indicated.",
            "Avoid unnecessary pesticide applications.",
            "Maintain normal crop nutrition.",
            "Maintain suitable irrigation.",
            "Consult an expert if symptoms appear."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Maintain field sanitation.",
            "Monitor leaves and fruit.",
            "Avoid prolonged leaf wetness.",
            "Remove severely damaged material when appropriate."
        ]
    },

    "Tomato_Bacterial_Spot": {
        "plant": "Tomato",
        "disease": "Bacterial Spot",
        "causes": [
            "Caused by bacterial pathogens in the Xanthomonas group.",
            "Rain and water splash can spread bacteria.",
            "Contaminated seed or planting material can introduce infection.",
            "Warm and wet conditions favor disease development.",
            "Wounds can provide entry points for bacteria."
        ],
        "medicine": [
            "Remove severely infected leaves where practical.",
            "Use locally registered copper-based products when recommended.",
            "Other registered products may be available in some regions.",
            "Avoid excessive repeated copper use.",
            "Follow the tomato-specific label and local agricultural advice."
        ],
        "prevention": [
            "Use certified disease-free seed and seedlings.",
            "Avoid unnecessary overhead irrigation.",
            "Maintain good plant spacing.",
            "Remove severely infected plant material.",
            "Sanitize tools and equipment where practical."
        ]
    },

    "Tomato_Early_Blight": {
        "plant": "Tomato",
        "disease": "Early Blight",
        "causes": [
            "Commonly associated with Alternaria species.",
            "Older leaves may develop brown lesions with concentric rings.",
            "Spores can spread through wind and rain.",
            "Plant stress may increase disease severity.",
            "Warm conditions and leaf wetness can favor disease."
        ],
        "medicine": [
            "Remove severely affected leaves where practical.",
            "Use a locally registered fungicide when recommended.",
            "Rotate fungicide modes of action where applicable.",
            "Avoid unnecessary chemical applications.",
            "Follow crop-specific labels and local guidance."
        ],
        "prevention": [
            "Use healthy seedlings.",
            "Maintain balanced nutrition.",
            "Avoid prolonged leaf wetness.",
            "Remove infected plant debris where appropriate.",
            "Scout lower leaves regularly."
        ]
    },

    "Tomato_Healthy": {
        "plant": "Tomato",
        "disease": "Healthy",
        "causes": [
            "No visible disease symptoms were detected.",
            "The image matches the healthy tomato class.",
            "No obvious bacterial, fungal or viral pattern was detected.",
            "The plant appears visually healthy.",
            "Regular monitoring is still recommended."
        ],
        "medicine": [
            "No disease medicine is indicated.",
            "Avoid unnecessary pesticide application.",
            "Maintain balanced plant nutrition.",
            "Maintain suitable irrigation.",
            "Consult an expert if symptoms develop."
        ],
        "prevention": [
            "Use healthy seedlings.",
            "Maintain field sanitation.",
            "Monitor leaves regularly.",
            "Control pests appropriately.",
            "Maintain suitable irrigation and nutrition."
        ]
    },

    "Tomato_Late_Blight": {
        "plant": "Tomato",
        "disease": "Late Blight",
        "causes": [
            "Caused by Phytophthora infestans.",
            "Cool and wet conditions favor disease development.",
            "Wind and rain can spread spores.",
            "Infected plant debris can provide inoculum.",
            "Dense and wet foliage can increase disease pressure."
        ],
        "medicine": [
            "Use a locally registered late-blight fungicide when recommended.",
            "Protectant fungicides can be part of integrated management.",
            "Rotate fungicide modes of action to reduce resistance risk.",
            "Remove infected debris where appropriate.",
            "Follow the tomato-specific product label and local recommendations."
        ],
        "prevention": [
            "Use healthy seedlings.",
            "Scout plants frequently.",
            "Avoid prolonged leaf wetness.",
            "Provide adequate plant spacing and airflow.",
            "Remove infected debris after the crop cycle."
        ]
    },

    "Tomato_Septoria_Leaf_Spot": {
        "plant": "Tomato",
        "disease": "Septoria Leaf Spot",
        "causes": [
            "Caused by the fungus Septoria lycopersici.",
            "Rain splash can spread fungal spores.",
            "Wet foliage favors infection.",
            "Infected plant debris can carry the pathogen.",
            "Dense foliage can increase humidity."
        ],
        "medicine": [
            "Remove heavily infected lower leaves.",
            "Use a locally registered fungicide when recommended.",
            "Rotate fungicide modes of action.",
            "Avoid unnecessary overhead irrigation.",
            "Follow the tomato-specific product label."
        ],
        "prevention": [
            "Remove infected plant debris.",
            "Use healthy seedlings.",
            "Maintain good plant spacing.",
            "Avoid prolonged leaf wetness.",
            "Scout lower leaves regularly."
        ]
    },

    "Tomato_Target_Spot": {
        "plant": "Tomato",
        "disease": "Target Spot",
        "causes": [
            "Associated with fungal pathogens including Corynespora cassiicola.",
            "Warm and humid conditions favor disease development.",
            "Rain splash can spread spores.",
            "Dense foliage can retain moisture.",
            "Infected plant debris can contribute to disease pressure."
        ],
        "medicine": [
            "Remove severely infected leaves where practical.",
            "Use a locally registered fungicide when recommended.",
            "Rotate fungicide modes of action.",
            "Improve canopy airflow.",
            "Follow product label directions and local recommendations."
        ],
        "prevention": [
            "Use healthy seedlings.",
            "Maintain adequate plant spacing.",
            "Avoid prolonged leaf wetness.",
            "Remove infected debris.",
            "Scout plants regularly."
        ]
    },

    "Tomato_Yellow_Leaf_Curl_Virus": {
        "plant": "Tomato",
        "disease": "Tomato Yellow Leaf Curl Virus",
        "causes": [
            "Caused by Tomato yellow leaf curl virus.",
            "Whiteflies are important insect vectors.",
            "Infected plants can serve as virus sources.",
            "Weeds can sometimes act as alternative hosts.",
            "Warm conditions can support whitefly populations."
        ],
        "medicine": [
            "There is no curative medicine that removes the virus from an infected plant.",
            "Control whitefly vectors using locally registered products when recommended.",
            "Remove severely infected plants where local guidance recommends removal.",
            "Use integrated insect-management strategies.",
            "Follow local pesticide labels and resistance-management recommendations."
        ],
        "prevention": [
            "Use virus-free certified seedlings.",
            "Monitor and manage whiteflies.",
            "Use suitable insect-exclusion methods where practical.",
            "Remove infected plants and weed hosts where recommended.",
            "Inspect plants regularly for early symptoms."
        ]
    }
}


# ============================================================
# FALLBACK ADVISORY
# ============================================================

DEFAULT_INFO = {
    "plant": "Plant",
    "disease": "Plant Disease",
    "causes": [
        "The model detected a disease pattern in the submitted image.",
        "The exact causal organism should be confirmed by field diagnosis.",
        "Environmental conditions can influence disease development.",
        "Plant stress may increase disease severity.",
        "Expert confirmation may be required."
    ],
    "medicine": [
        "Do not apply chemicals without confirming the disease.",
        "Use only products registered for the crop and disease.",
        "Follow the product label exactly.",
        "Consult a local agricultural expert before chemical treatment.",
        "Monitor the plant after treatment."
    ],
    "prevention": [
        "Use healthy planting material.",
        "Maintain good field sanitation.",
        "Monitor plants regularly.",
        "Maintain appropriate irrigation and nutrition.",
        "Seek expert confirmation if symptoms increase."
    ]
}


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_image(image_path):
    try:
        image_path = Path(image_path)

        if not image_path.is_file():
            return {
                "success": False,
                "error": f"Image file not found: {image_path}"
            }

        with Image.open(image_path) as source_image:
            image = source_image.convert("RGB")

        input_tensor = transform(image).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)

            confidence, predicted_index = torch.max(
                probabilities, dim=1
            )

            top_values, top_indices = torch.topk(
                probabilities,
                min(5, NUM_CLASSES),
                dim=1
            )

        predicted_index = predicted_index.item()
        confidence = confidence.item() * 100
        predicted_class = CLASSES[predicted_index]

        info = DISEASE_INFO.get(predicted_class, DEFAULT_INFO)

        if confidence >= 70:
            confidence_level = "High"
            confidence_message = (
                "The model has high confidence in this prediction. "
                "Confirm the result by inspecting the plant."
            )
        elif confidence >= 50:
            confidence_level = "Moderate"
            confidence_message = (
                "The model has moderate confidence. "
                "Field verification is recommended."
            )
        else:
            confidence_level = "Low"
            confidence_message = (
                "The model has low confidence. "
                "Verify the image and consult an expert."
            )

        top_predictions = []

        for value, index in zip(top_values[0], top_indices[0]):
            top_predictions.append({
                "class": CLASSES[index.item()],
                "confidence": round(value.item() * 100, 2)
            })

        return {
            "success": True,
            "model": "EfficientNet-B0",
            "classes": NUM_CLASSES,
            "test_accuracy": round(TEST_ACCURACY, 2),
            "predicted_class": predicted_class,
            "plant": info["plant"],
            "disease": info["disease"],
            "confidence": round(confidence, 2),
            "confidence_level": confidence_level,
            "confidence_message": confidence_message,
            "causes": info["causes"],
            "medicine": info["medicine"],
            "treatment": info["medicine"],
            "prevention": info["prevention"],
            "suggestions": info["prevention"],
            "top_predictions": top_predictions
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================
# COMMAND LINE TEST
# ============================================================

if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("PLANTCARE AI - 38 CLASS MODEL")
    print("=" * 60)
    print("Device       :", DEVICE)
    print("Classes      :", NUM_CLASSES)
    print("Test Accuracy:", TEST_ACCURACY)
    print()

    if len(sys.argv) < 2:
        print('Usage: python backend/predict.py "path_to_leaf_image"')
        sys.exit(0)

    result = predict_image(sys.argv[1])

    if not result.get("success"):
        print("Prediction failed:", result.get("error"))
        sys.exit(1)

    print("Plant       :", result["plant"])
    print("Disease     :", result["disease"])
    print("Confidence  :", result["confidence"], "%")
    print("Test Acc.   :", result["test_accuracy"], "%")

    print("\nCAUSES")
    for point in result["causes"]:
        print("-", point)

    print("\nMEDICINE / TREATMENT")
    for point in result["medicine"]:
        print("-", point)

    print("\nPREVENTION")
    for point in result["prevention"]:
        print("-", point)

    print("\nTOP PREDICTIONS")
    for item in result["top_predictions"]:
        print(
            f"- {item['class']}: {item['confidence']}%"
        )

    print("=" * 60)
