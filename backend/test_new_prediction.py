import os
import json
import sys

import torch
from PIL import Image
from torchvision import transforms, models


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "new_plant_model_best.pth"
)

CLASSES_PATH = os.path.join(
    BASE_DIR,
    "model",
    "new_plant_classes.json"
)


# ============================================================
# SETTINGS
# ============================================================

IMAGE_SIZE = 224

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)


# ============================================================
# LOAD CLASSES
# ============================================================

with open(
    CLASSES_PATH,
    "r",
    encoding="utf-8"
) as f:

    classes = json.load(f)


# ============================================================
# LOAD MODEL
# ============================================================

model = models.efficientnet_b0(
    weights=None
)

in_features = model.classifier[1].in_features

model.classifier[1] = torch.nn.Linear(
    in_features,
    len(classes)
)

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE,
    weights_only=True
)

if (
    isinstance(checkpoint, dict)
    and "model_state_dict" in checkpoint
):

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

else:

    model.load_state_dict(
        checkpoint
    )

model = model.to(DEVICE)
model.eval()


# ============================================================
# IMAGE TRANSFORM
# ============================================================

transform = transforms.Compose([
    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],

        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_image(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")

    image_tensor = transform(
        image
    ).unsqueeze(0)

    image_tensor = image_tensor.to(
        DEVICE
    )

    with torch.no_grad():

        outputs = model(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

    class_index = prediction.item()

    disease = classes[
        class_index
    ]

    confidence_value = (
        confidence.item() * 100
    )

    # Top 3 predictions
    top_probabilities, top_indices = torch.topk(
        probabilities,
        min(3, len(classes))
    )

    top_predictions = []

    for probability, index in zip(
        top_probabilities[0],
        top_indices[0]
    ):

        top_predictions.append({
            "class": classes[index.item()],
            "confidence": round(
                probability.item() * 100,
                2
            )
        })

    return {
        "disease": disease,
        "confidence": round(
            confidence_value,
            2
        ),
        "top_predictions": top_predictions
    }


# ============================================================
# MAIN
# ============================================================

print()
print("=" * 70)
print("NEW PLANT DISEASE PREDICTION")
print("=" * 70)

print()
print("Device :", DEVICE)
print("Classes:", len(classes))
print()


# ============================================================
# GET IMAGE PATH
# ============================================================

if len(sys.argv) >= 2:

    image_path = sys.argv[1]

else:

    image_path = input(
        "Enter image path: "
    ).strip().strip('"')


# ============================================================
# CHECK IMAGE
# ============================================================

if not os.path.exists(image_path):

    print()
    print("ERROR: Image not found.")
    print(
        "Path:",
        image_path
    )

    sys.exit(1)


# ============================================================
# PREDICT
# ============================================================

try:

    result = predict_image(
        image_path
    )

except Exception as e:

    print()
    print("Prediction error:")
    print(e)

    sys.exit(1)


# ============================================================
# DISPLAY
# ============================================================

print()
print("=" * 70)
print("PREDICTION RESULT")
print("=" * 70)

print()
print(
    "Disease / Class :",
    result["disease"]
)

print(
    "Confidence      :",
    f'{result["confidence"]:.2f}%'
)

print()

print("TOP 3 PREDICTIONS")
print("-" * 40)

for item in result["top_predictions"]:

    print(
        f'{item["class"]} '
        f'-> {item["confidence"]:.2f}%'
    )

print()
print("=" * 70)