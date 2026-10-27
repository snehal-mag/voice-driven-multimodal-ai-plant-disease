import os
import json
import torch
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_DIR = os.path.join(
    BASE_DIR,
    "new_plant_training_dataset",
    "test"
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

RESULT_PATH = os.path.join(
    BASE_DIR,
    "model",
    "new_plant_test_results.json"
)

# ============================================================
# SETTINGS
# ============================================================

IMAGE_SIZE = 224
BATCH_SIZE = 16

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=" * 70)
print("NEW PLANT DISEASE MODEL - TEST EVALUATION")
print("=" * 70)

print()
print("Device :", DEVICE)
print("Test dataset :", TEST_DIR)
print()

# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(TEST_DIR):
    raise FileNotFoundError(
        f"Test dataset not found:\n{TEST_DIR}"
    )

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model not found:\n{MODEL_PATH}"
    )

if not os.path.exists(CLASSES_PATH):
    raise FileNotFoundError(
        f"Classes file not found:\n{CLASSES_PATH}"
    )

# ============================================================
# LOAD CLASSES
# ============================================================

with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    classes = json.load(f)

print("Number of classes :", len(classes))

print()
print("Classes:")

for i, class_name in enumerate(classes):
    print(f"{i:2d}: {class_name}")

# ============================================================
# TRANSFORM
# ============================================================

test_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ============================================================
# DATASET
# ============================================================

print()
print("Loading test dataset...")

test_dataset = datasets.ImageFolder(
    TEST_DIR,
    transform=test_transform
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

print("Test images :", len(test_dataset))

# ============================================================
# MODEL
# ============================================================

print()
print("=" * 70)
print("LOADING EFFICIENTNET-B0")
print("=" * 70)

model = models.efficientnet_b0(weights=None)

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

if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
    model.load_state_dict(checkpoint["model_state_dict"])
else:
    model.load_state_dict(checkpoint)

model = model.to(DEVICE)
model.eval()

print("Model loaded successfully.")

# ============================================================
# PREDICTION
# ============================================================

all_predictions = []
all_labels = []

correct = 0
total = 0

print()
print("Running predictions...")

with torch.no_grad():

    for batch_index, (images, labels) in enumerate(test_loader):

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        outputs = model(images)

        predictions = torch.argmax(
            outputs,
            dim=1
        )

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

        all_predictions.extend(
            predictions.cpu().numpy()
        )

        all_labels.extend(
            labels.cpu().numpy()
        )

        if (batch_index + 1) % 20 == 0:
            print(
                f"Processed batches: "
                f"{batch_index + 1}/{len(test_loader)}"
            )

# ============================================================
# ACCURACY
# ============================================================

accuracy = (
    correct / total
) * 100

# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 70)
print("FINAL TEST RESULT")
print("=" * 70)

print()
print("Test Images :", total)
print("Correct     :", correct)
print("Incorrect   :", total - correct)
print(f"TEST ACCURACY : {accuracy:.2f}%")

# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print()
print("=" * 70)
print("CLASS-WISE PERFORMANCE")
print("=" * 70)

report = classification_report(
    all_labels,
    all_predictions,
    target_names=classes,
    output_dict=True,
    zero_division=0
)

print(
    classification_report(
        all_labels,
        all_predictions,
        target_names=classes,
        zero_division=0
    )
)

# ============================================================
# CONFUSION MATRIX
# ============================================================

matrix = confusion_matrix(
    all_labels,
    all_predictions
)

print()
print("=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)

print(matrix)

# ============================================================
# SAVE RESULTS
# ============================================================

results = {
    "model": "EfficientNet-B0",
    "device": str(DEVICE),
    "num_classes": len(classes),
    "test_images": total,
    "correct": correct,
    "incorrect": total - correct,
    "test_accuracy": accuracy,
    "classes": classes,
    "classification_report": report,
    "confusion_matrix": matrix.tolist()
}

with open(
    RESULT_PATH,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        indent=4
    )

print()
print("=" * 70)
print("RESULTS SAVED")
print("=" * 70)

print()
print(
    f"Results saved to:\n{RESULT_PATH}"
)

print()
print("=" * 70)
print("EVALUATION COMPLETE")
print("=" * 70)