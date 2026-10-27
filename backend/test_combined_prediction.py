import sys
import json
from pathlib import Path

import torch
from torch import nn
from torchvision import models, transforms
from PIL import Image


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "model" / "combined_30_model_best.pth"
CLASSES_PATH = BASE_DIR / "model" / "combined_30_classes.json"


# ============================================================
# SETTINGS
# ============================================================

IMAGE_SIZE = 224
TOP_K = 5


# ============================================================
# DEVICE
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# CHECK IMAGE ARGUMENT
# ============================================================

if len(sys.argv) < 2:
    print()
    print("=" * 70)
    print("ERROR: Please provide an image path.")
    print("=" * 70)
    print()
    print("Example:")
    print(
        r'.\venv\Scripts\python.exe backend\test_combined_prediction.py ".\combined_training_dataset\test\Apple___Apple_scab\image.JPG"'
    )
    print()
    sys.exit(1)


IMAGE_PATH = Path(sys.argv[1])

if not IMAGE_PATH.is_absolute():
    IMAGE_PATH = (Path.cwd() / IMAGE_PATH).resolve()


# ============================================================
# CHECK FILES
# ============================================================

if not IMAGE_PATH.exists():
    print()
    print("ERROR: Image file not found:")
    print(IMAGE_PATH)
    print()
    sys.exit(1)

if not MODEL_PATH.exists():
    print("ERROR: Model not found:")
    print(MODEL_PATH)
    sys.exit(1)

if not CLASSES_PATH.exists():
    print("ERROR: Classes file not found:")
    print(CLASSES_PATH)
    sys.exit(1)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("30-CLASS PLANT DISEASE IMAGE PREDICTION")
print("=" * 70)

print()
print("Device :", device)
print("Image  :", IMAGE_PATH)
print()


# ============================================================
# LOAD CLASSES
# ============================================================

with open(
    CLASSES_PATH,
    "r",
    encoding="utf-8"
) as f:

    classes = json.load(f)

print("Number of classes :", len(classes))


# ============================================================
# IMAGE TRANSFORM
# ============================================================

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ============================================================
# LOAD MODEL
# ============================================================

print()
print("Loading EfficientNet-B0...")

model = models.efficientnet_b0(weights=None)

num_features = model.classifier[1].in_features

model.classifier = nn.Sequential(
    nn.Dropout(0.3),
    nn.Linear(num_features, len(classes))
)

checkpoint = torch.load(
    MODEL_PATH,
    map_location=device,
    weights_only=True
)

model.load_state_dict(checkpoint)

model = model.to(device)
model.eval()

print("Model loaded successfully.")


# ============================================================
# LOAD IMAGE
# ============================================================

try:

    image = Image.open(IMAGE_PATH).convert("RGB")

except Exception as e:

    print()
    print("ERROR: Could not open image.")
    print(str(e))
    sys.exit(1)


input_tensor = transform(image)
input_tensor = input_tensor.unsqueeze(0)
input_tensor = input_tensor.to(device)


# ============================================================
# PREDICTION
# ============================================================

with torch.no_grad():

    outputs = model(input_tensor)

    probabilities = torch.softmax(
        outputs,
        dim=1
    )[0]

    top_probabilities, top_indices = torch.topk(
        probabilities,
        min(TOP_K, len(classes))
    )


# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 70)
print("PREDICTION RESULT")
print("=" * 70)

top_index = top_indices[0].item()
top_confidence = top_probabilities[0].item() * 100

print()
print("Predicted class :", classes[top_index])
print(f"Confidence      : {top_confidence:.2f}%")


print()
print("=" * 70)
print("TOP 5 PREDICTIONS")
print("=" * 70)

for rank, (probability, index) in enumerate(
    zip(top_probabilities, top_indices),
    start=1
):

    class_name = classes[index.item()]
    confidence = probability.item() * 100

    print(
        f"{rank}. {class_name:<55} {confidence:.2f}%"
    )


# ============================================================
# SAFETY INFORMATION
# ============================================================

print()
print("=" * 70)
print("PREDICTION INTERPRETATION")
print("=" * 70)

if top_confidence >= 70:

    print(
        "High-confidence prediction."
    )

elif top_confidence >= 50:

    print(
        "Moderate-confidence prediction."
    )
    print(
        "Consider providing a clearer leaf image."
    )

else:

    print(
        "Low-confidence prediction."
    )
    print(
        "The image may be unclear or outside the supported classes."
    )


print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
