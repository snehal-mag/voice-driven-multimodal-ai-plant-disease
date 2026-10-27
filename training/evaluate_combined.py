import json
from pathlib import Path

import torch
from torch import nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEST_DIR = BASE_DIR / "combined_training_dataset" / "test"

MODEL_PATH = BASE_DIR / "model" / "combined_30_model_best.pth"
CLASSES_PATH = BASE_DIR / "model" / "combined_30_classes.json"

RESULT_PATH = BASE_DIR / "model" / "combined_30_test_results.json"


# ============================================================
# SETTINGS
# ============================================================

IMAGE_SIZE = 224
BATCH_SIZE = 16


# ============================================================
# DEVICE
# ============================================================

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


print("=" * 70)
print("UNIFIED 30-CLASS PLANT DISEASE MODEL - TEST EVALUATION")
print("=" * 70)

print()
print("Device :", device)
print("Test dataset :", TEST_DIR)
print()


# ============================================================
# LOAD CLASSES
# ============================================================

with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    classes = json.load(f)

print("Number of classes :", len(classes))
print()

for i, class_name in enumerate(classes):
    print(f"{i:2d}: {class_name}")


# ============================================================
# TRANSFORMS
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
# LOAD TEST DATASET
# ============================================================

print()
print("=" * 70)
print("LOADING TEST DATASET")
print("=" * 70)

test_dataset = datasets.ImageFolder(
    str(TEST_DIR),
    transform=test_transform
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

print()
print("Test images :", len(test_dataset))


# ============================================================
# CHECK CLASS ORDER
# ============================================================

if test_dataset.classes != classes:
    print()
    print("WARNING: Dataset class order and saved class order differ.")

    print("Dataset classes:")
    for i, name in enumerate(test_dataset.classes):
        print(i, name)

    print()
    print("Saved classes:")
    for i, name in enumerate(classes):
        print(i, name)


# ============================================================
# LOAD EFFICIENTNET-B0
# ============================================================

print()
print("=" * 70)
print("LOADING EFFICIENTNET-B0")
print("=" * 70)

model = models.efficientnet_b0(weights=None)

num_features = model.classifier[1].in_features

model.classifier = nn.Sequential(
    nn.Dropout(p=0.3),
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

print()
print("Model loaded successfully.")


# ============================================================
# PREDICTION
# ============================================================

print()
print("=" * 70)
print("RUNNING TEST PREDICTIONS")
print("=" * 70)

all_predictions = []
all_labels = []

correct = 0
total = 0

with torch.no_grad():

    for batch_index, (images, labels) in enumerate(test_loader):

        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)

        predictions = torch.argmax(outputs, dim=1)

        correct += (predictions == labels).sum().item()
        total += labels.size(0)

        all_predictions.extend(
            predictions.cpu().numpy().tolist()
        )

        all_labels.extend(
            labels.cpu().numpy().tolist()
        )

        if (batch_index + 1) % 20 == 0:
            print(
                f"Batch {batch_index + 1}/{len(test_loader)}"
            )


# ============================================================
# TEST ACCURACY
# ============================================================

accuracy = (correct / total) * 100

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

report_text = classification_report(
    all_labels,
    all_predictions,
    target_names=classes,
    digits=2,
    zero_division=0
)

print()
print(report_text)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    all_labels,
    all_predictions,
    labels=list(range(len(classes)))
)

print("=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)

print()

for row in cm:
    print(row.tolist())


# ============================================================
# SAVE RESULTS
# ============================================================

results = {
    "model": "EfficientNet-B0",
    "number_of_classes": len(classes),
    "test_images": total,
    "correct": correct,
    "incorrect": total - correct,
    "test_accuracy": round(accuracy, 2),
    "classes": classes,
    "classification_report": classification_report(
        all_labels,
        all_predictions,
        target_names=classes,
        output_dict=True,
        zero_division=0
    ),
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


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 70)
print("EVALUATION COMPLETE")
print("=" * 70)

print()
print("Results saved to:")
print(RESULT_PATH)

print()
print("=" * 70)