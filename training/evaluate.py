import os
import json
import torch
from torch import nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

TEST_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "test"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "model"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "plant_disease_model_best.pth"
)

CLASSES_PATH = os.path.join(
    MODEL_DIR,
    "classes.json"
)

RESULT_PATH = os.path.join(
    MODEL_DIR,
    "test_results.json"
)

# ============================================================
# CONFIG
# ============================================================

IMAGE_SIZE = 224
BATCH_SIZE = 16

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("PLANT DISEASE MODEL - TEST EVALUATION")
print("=" * 70)

print(f"Device : {DEVICE}")

# ============================================================
# TRANSFORM
# ============================================================

test_transform = transforms.Compose([
    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ============================================================
# DATASET
# ============================================================

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

classes = test_dataset.classes

print("\nTest Dataset")
print("-" * 70)
print(f"Test images : {len(test_dataset)}")
print(f"Classes     : {len(classes)}")

for i, class_name in enumerate(classes):
    print(f"{i}: {class_name}")

# ============================================================
# MODEL
# ============================================================

print("\nLoading EfficientNet-B0...")

model = models.efficientnet_b0(
    weights=None
)

in_features = model.classifier[1].in_features

model.classifier = nn.Sequential(
    nn.Dropout(0.3),
    nn.Linear(
        in_features,
        len(classes)
    )
)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )
)

model = model.to(DEVICE)
model.eval()

print("Model loaded successfully.")

# ============================================================
# PREDICTION
# ============================================================

all_labels = []
all_predictions = []

correct = 0
total = 0

print("\nRunning evaluation...")

with torch.no_grad():

    for images, labels in test_loader:

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

        all_labels.extend(
            labels.cpu().numpy()
        )

        all_predictions.extend(
            predictions.cpu().numpy()
        )

# ============================================================
# ACCURACY
# ============================================================

accuracy = accuracy_score(
    all_labels,
    all_predictions
)

accuracy_percent = accuracy * 100

print("\n" + "=" * 70)
print("FINAL TEST RESULT")
print("=" * 70)

print(f"\nTest Images : {total}")
print(f"Correct     : {correct}")
print(f"Incorrect   : {total - correct}")

print(
    f"\nTEST ACCURACY : "
    f"{accuracy_percent:.2f}%"
)

# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 70)
print("CLASS-WISE PERFORMANCE")
print("=" * 70)

report = classification_report(
    all_labels,
    all_predictions,
    target_names=classes,
    digits=2,
    zero_division=0
)

print(report)

# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    all_labels,
    all_predictions
)

print("=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)

print(cm)

# ============================================================
# SAVE RESULTS
# ============================================================

results = {
    "test_images": total,
    "correct": correct,
    "incorrect": total - correct,
    "test_accuracy": round(
        accuracy_percent,
        2
    ),
    "classes": classes,
    "confusion_matrix": cm.tolist()
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

print("\nResults saved to:")
print(RESULT_PATH)

print("\n" + "=" * 70)
print("EVALUATION COMPLETED")
print("=" * 70)
