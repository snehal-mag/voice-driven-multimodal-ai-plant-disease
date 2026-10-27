# ============================================================
# PLANTCARE AI - PREDICTION + 5 POINT ADVISORY SYSTEM
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

MODEL_PATH = MODEL_DIR / "combined_30_model_best.pth"
CLASSES_PATH = MODEL_DIR / "combined_30_classes.json"
RESULTS_PATH = MODEL_DIR / "combined_30_test_results.json"


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ============================================================
# LOAD CLASSES
# ============================================================

with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    CLASSES = json.load(f)

NUM_CLASSES = len(CLASSES)


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

TEST_ACCURACY = 96.99

try:
    if RESULTS_PATH.exists():

        with open(RESULTS_PATH, "r", encoding="utf-8") as f:
            results = json.load(f)

        if "accuracy" in results:
            TEST_ACCURACY = float(results["accuracy"])

        elif "test_accuracy" in results:
            TEST_ACCURACY = float(results["test_accuracy"])

except Exception:
    TEST_ACCURACY = 96.99


# ============================================================
# DISEASE INFORMATION
#
# Every disease contains:
# 5 causes
# 5 medicine/treatment points
# 5 prevention points
# ============================================================

DISEASE_INFO = {

    # ========================================================
    # APPLE
    # ========================================================

    "Apple___Apple_scab": {

        "plant": "Apple",
        "disease": "Apple Scab",

        "causes": [
            "Caused mainly by the fungus Venturia inaequalis.",
            "Wet leaves and humid conditions favor infection.",
            "Rain splash and air movement can spread fungal spores.",
            "Infected fallen leaves can produce new spores.",
            "Young leaves and developing fruit are highly susceptible."
        ],

        "medicine": [
            "Remove severely infected leaves and fruit where practical.",
            "Improve canopy airflow through appropriate pruning.",
            "Use a locally registered apple-scab fungicide when recommended.",
            "Fungicide active ingredients should be rotated to reduce resistance risk.",
            "Always follow the crop-specific product label and local agricultural advice."
        ],

        "prevention": [
            "Use resistant apple varieties where available.",
            "Remove or manage infected fallen leaves.",
            "Maintain good air circulation inside the canopy.",
            "Avoid unnecessary prolonged leaf wetness.",
            "Inspect new leaves regularly for early symptoms."
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
            "Follow the product label and local agricultural recommendations."
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
        "disease": "Apple Cedar Rust",

        "causes": [
            "Caused by Gymnosporangium rust fungi.",
            "The disease involves alternate cedar or juniper hosts.",
            "Spores can move between alternate host plants.",
            "Wet spring conditions can favor infection.",
            "Young leaves and fruit can be susceptible."
        ],

        "medicine": [
            "Remove severely affected plant material where practical.",
            "Manage alternate hosts where locally appropriate.",
            "Improve airflow around the tree canopy.",
            "Use a locally registered rust fungicide when recommended.",
            "Follow label instructions and resistance-management guidance."
        ],

        "prevention": [
            "Use resistant cultivars where available.",
            "Monitor trees during periods favorable for rust.",
            "Maintain orchard sanitation.",
            "Avoid excessively dense canopy growth.",
            "Manage alternate hosts according to local recommendations."
        ]
    },


    "Apple___healthy": {

        "plant": "Apple",
        "disease": "Healthy",

        "causes": [
            "No visible disease symptoms were detected.",
            "Leaves appear consistent with the healthy class used by the model.",
            "No obvious disease lesion was identified by the classifier.",
            "The plant may currently be in a healthy condition.",
            "Image quality can affect the reliability of visual classification."
        ],

        "medicine": [
            "No disease medicine is indicated from this prediction.",
            "Do not apply fungicide or insecticide without a confirmed problem.",
            "Maintain normal crop nutrition.",
            "Continue regular plant monitoring.",
            "Consult an agricultural expert if symptoms appear later."
        ],

        "prevention": [
            "Use healthy planting material.",
            "Maintain proper irrigation.",
            "Maintain balanced plant nutrition.",
            "Monitor leaves and fruit regularly.",
            "Maintain good orchard sanitation."
        ]
    },


    # ========================================================
    # BLUEBERRY
    # ========================================================

    "Blueberry___healthy": {

        "plant": "Blueberry",
        "disease": "Healthy",

        "causes": [
            "No visible disease symptoms were detected.",
            "The image matches the healthy blueberry class.",
            "No obvious leaf disease pattern was detected.",
            "The plant appears visually healthy in the submitted image.",
            "Environmental stress may still exist without visible symptoms."
        ],

        "medicine": [
            "No disease medicine is indicated from this prediction.",
            "Avoid unnecessary pesticide applications.",
            "Maintain suitable soil moisture.",
            "Maintain appropriate crop nutrition.",
            "Seek expert diagnosis if new symptoms develop."
        ],

        "prevention": [
            "Use healthy planting material.",
            "Maintain good field sanitation.",
            "Monitor leaves regularly.",
            "Maintain suitable soil conditions.",
            "Remove severely damaged plant material when appropriate."
        ]
    },


    # ========================================================
    # CHERRY
    # ========================================================

    "Cherry_(including_sour)___Powdery_mildew": {

        "plant": "Cherry",
        "disease": "Cherry Powdery Mildew",

        "causes": [
            "Caused by powdery mildew fungi.",
            "The pathogen produces white powder-like growth.",
            "Humid conditions can favor disease development.",
            "Dense foliage can reduce air movement.",
            "Spores can spread through air movement."
        ],

        "medicine": [
            "Remove severely affected plant tissue where practical.",
            "Improve canopy ventilation through suitable pruning.",
            "Use a locally registered powdery-mildew fungicide when recommended.",
            "Sulfur or other registered products may be options depending on local rules.",
            "Follow crop-specific label directions."
        ],

        "prevention": [
            "Maintain good canopy ventilation.",
            "Avoid excessive nitrogen fertilization.",
            "Monitor young leaves regularly.",
            "Remove severely infected plant material.",
            "Use tolerant varieties where available."
        ]
    },


    "Cherry_(including_sour)___healthy": {

        "plant": "Cherry",
        "disease": "Healthy",

        "causes": [
            "No visible disease symptoms were detected.",
            "The image matches the healthy cherry class.",
            "No obvious disease lesion was identified.",
            "The plant appears visually healthy in the submitted image.",
            "Continued monitoring is still recommended."
        ],

        "medicine": [
            "No disease medicine is indicated.",
            "Avoid unnecessary fungicide applications.",
            "Maintain normal plant nutrition.",
            "Maintain proper irrigation.",
            "Seek expert diagnosis if symptoms appear."
        ],

        "prevention": [
            "Use healthy planting material.",
            "Maintain good orchard sanitation.",
            "Monitor leaves and fruit.",
            "Maintain good canopy airflow.",
            "Remove damaged plant material when appropriate."
        ]
    },


    # ========================================================
    # CORN
    # ========================================================

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
            "Use a locally registered corn fungicide when economically justified.",
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


    # ========================================================
    # GRAPE
    # ========================================================

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


    # ========================================================
    # ORANGE
    # ========================================================

    "Orange___Haunglongbing_(Citrus_greening)": {

        "plant": "Orange",
        "disease": "Citrus Greening / Huanglongbing",

        "causes": [
            "Associated with Candidatus Liberibacter bacteria.",
            "The disease is mainly spread by citrus psyllid insect vectors.",
            "Infected planting material can spread the pathogen.",
            "Infected trees can act as sources of infection.",
            "The disease can cause leaf mottling, decline and poor fruit development."
        ],

        "medicine": [
            "There is currently no curative medicine that eliminates HLB from an infected tree.",
            "Manage citrus psyllid populations using locally registered products when recommended.",
            "Rotate insecticide modes of action according to local guidance.",
            "Remove infected trees where local agricultural authorities recommend removal.",
            "Follow local pesticide labels and citrus disease-management recommendations."
        ],

        "prevention": [
            "Use certified healthy planting material.",
            "Monitor new plant growth for psyllids.",
            "Regularly inspect trees for symptoms.",
            "Control psyllid populations according to local recommendations.",
            "Follow applicable quarantine and plant-movement requirements."
        ]
    },


    # ========================================================
    # PEACH
    # ========================================================

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
            "Avoid unnecessary repeated copper applications because resistance and crop injury can occur.",
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
            "Continued monitoring is still recommended."
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


    # ========================================================
    # PEPPER
    # ========================================================

    "Pepper_Healthy": {

        "plant": "Pepper",
        "disease": "Pepper Healthy",

        "causes": [
            "No visible disease symptoms were detected.",
            "The image matches the healthy pepper class.",
            "No obvious bacterial, fungal or viral pattern was detected.",
            "The plant appears visually healthy.",
            "Hidden stress may still exist without visible leaf symptoms."
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


    # ========================================================
    # POTATO
    # ========================================================

    "Potato_Late_Blight": {

        "plant": "Potato",
        "disease": "Potato Late Blight",

        "causes": [
            "Caused by the oomycete Phytophthora infestans.",
            "Cool and wet conditions can strongly favor disease development.",
            "Spores can spread through wind and rain.",
            "Infected plant debris or tubers can carry inoculum.",
            "Rapid disease development can occur under favorable weather."
        ],

        "medicine": [
            "Use a locally registered late-blight fungicide when recommended.",
            "Protectant fungicides may be used as part of an integrated program.",
            "Rotate fungicide modes of action to reduce resistance risk.",
            "Remove or manage severely infected plant material where appropriate.",
            "Follow the potato-specific product label and local agricultural guidance."
        ],

        "prevention": [
            "Use certified disease-free seed tubers.",
            "Scout fields frequently.",
            "Avoid excessive leaf wetness where possible.",
            "Destroy volunteer potatoes where appropriate.",
            "Follow local late-blight forecasting and management recommendations."
        ]
    },


    # ========================================================
    # RASPBERRY
    # ========================================================

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


    # ========================================================
    # SOYBEAN
    # ========================================================

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
            "Seek expert diagnosis if new symptoms develop."
        ],

        "prevention": [
            "Use healthy seed.",
            "Practice suitable crop rotation.",
            "Monitor plants regularly.",
            "Maintain balanced nutrition.",
            "Manage weeds and crop residue appropriately."
        ]
    },


    # ========================================================
    # STRAWBERRY
    # ========================================================

    "Strawberry___Leaf_scorch": {

        "plant": "Strawberry",
        "disease": "Strawberry Leaf Scorch",

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
            "Rotate fungicide modes of action where repeated treatment is required.",
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


    # ========================================================
    # TOMATO
    # ========================================================

    "Tomato_Bacterial_Spot": {

        "plant": "Tomato",
        "disease": "Tomato Bacterial Spot",

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
            "Some areas may permit other registered bacterial-disease products.",
            "Avoid excessive repeated copper use because resistance may develop.",
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


    "Tomato_Healthy": {

        "plant": "Tomato",
        "disease": "Tomato Healthy",

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
        "disease": "Tomato Late Blight",

        "causes": [
            "Caused by Phytophthora infestans.",
            "Cool and wet conditions favor disease development.",
            "Wind and rain can spread spores.",
            "Infected plant debris can provide inoculum.",
            "Dense and wet foliage can increase disease pressure."
        ],

        "medicine": [
            "Use a locally registered late-blight fungicide when recommended.",
            "Protectant fungicides can be part of an integrated disease-management program.",
            "Rotate fungicide modes of action to reduce resistance risk.",
            "Remove severely infected plant material where appropriate.",
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
        "disease": "Tomato Septoria Leaf Spot",

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
        "disease": "Tomato Target Spot",

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
            "Use insect-management strategies to reduce virus transmission.",
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
# FALLBACK
# ============================================================

DEFAULT_INFO = {

    "plant": "Plant",
    "disease": "Plant Disease",

    "causes": [
        "The model detected a disease pattern in the submitted image.",
        "The exact causal organism should be confirmed by field diagnosis.",
        "Environmental conditions can influence disease development.",
        "Plant stress may increase disease severity.",
        "Laboratory or expert confirmation may be required."
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

        # ----------------------------------------------------
        # OPEN IMAGE
        # ----------------------------------------------------

        image = Image.open(image_path).convert("RGB")

        input_tensor = transform(image).unsqueeze(0).to(DEVICE)

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        with torch.no_grad():

            outputs = model(input_tensor)

            probabilities = torch.softmax(outputs, dim=1)

            confidence, predicted_index = torch.max(
                probabilities,
                dim=1
            )

        predicted_index = predicted_index.item()

        confidence = confidence.item() * 100

        predicted_class = CLASSES[predicted_index]

        # ----------------------------------------------------
        # INFORMATION
        # ----------------------------------------------------

        info = DISEASE_INFO.get(
            predicted_class,
            DEFAULT_INFO
        )

        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        if confidence >= 70:
            confidence_level = "High"
            confidence_message = (
                "The model has high confidence in this prediction."
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
                "Please verify the image and consult an expert."
            )

        # ----------------------------------------------------
        # TOP PREDICTIONS
        # ----------------------------------------------------

        top_values, top_indices = torch.topk(
            probabilities,
            min(5, NUM_CLASSES),
            dim=1
        )

        top_predictions = []

        for value, index in zip(
            top_values[0],
            top_indices[0]
        ):

            top_predictions.append({
                "class": CLASSES[index.item()],
                "confidence": round(
                    value.item() * 100,
                    2
                )
            })

        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        return {

            "success": True,

            "model": "EfficientNet-B0",

            "classes": NUM_CLASSES,

            "test_accuracy": round(
                TEST_ACCURACY,
                2
            ),

            "predicted_class": predicted_class,

            "plant": info["plant"],

            "disease": info["disease"],

            "confidence": round(
                confidence,
                2
            ),

            "confidence_level": confidence_level,

            "confidence_message": confidence_message,

            # NEW STRUCTURED ADVISORY
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
    print("🌱 PLANTCARE AI")
    print("=" * 60)

    print("Device       :", DEVICE)
    print("Classes      :", NUM_CLASSES)
    print("Test Accuracy:", TEST_ACCURACY)
    print()

    if len(sys.argv) < 2:

        print(
            "Usage:"
        )

        print(
            'python backend/predict.py "image_path"'
        )

        sys.exit(0)

    image_path = sys.argv[1]

    result = predict_image(image_path)

    print(
        "Plant       :",
        result.get("plant")
    )

    print(
        "Disease     :",
        result.get("disease")
    )

    print(
        "Confidence  :",
        result.get("confidence"),
        "%"
    )

    print(
        "Test Acc.   :",
        result.get("test_accuracy"),
        "%"
    )

    print("\nCAUSES")

    for point in result.get("causes", []):
        print("•", point)

    print("\nMEDICINE / TREATMENT")

    for point in result.get("medicine", []):
        print("•", point)

    print("\nPREVENTION")

    for point in result.get("prevention", []):
        print("•", point)

    print("=" * 60)