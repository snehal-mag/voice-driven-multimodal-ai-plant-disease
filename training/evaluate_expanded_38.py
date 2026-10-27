
import json
from pathlib import Path

import torch
from torch import nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parent.parent
TEST_DIR = ROOT / "expanded_38_dataset" / "test"
MODEL_PATH = ROOT / "model" / "expanded_38_model_best.pth"
CLASSES_PATH = ROOT / "model" / "expanded_38_classes.json"
RESULT_PATH = ROOT / "model" / "expanded_38_test_results.json"
REPORT_PATH = ROOT / "model" / "expanded_38_classification_report.txt"

IMAGE_SIZE = 224
BATCH_SIZE = 16

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("=" * 60)
print("PLANTCARE AI - 38 CLASS TEST EVALUATION")
print("=" * 60)
print("Device:", device)

for path in [TEST_DIR, MODEL_PATH, CLASSES_PATH]:
    if not path.exists():
        raise FileNotFoundError(f"Required path not found: {path}")

with CLASSES_PATH.open(encoding="utf-8") as f:
    classes = json.load(f)

if len(classes) != 38:
    raise ValueError(f"Expected 38 classes, found {len(classes)}")

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

dataset = datasets.ImageFolder(str(TEST_DIR), transform=transform)

if dataset.classes != classes:
    raise ValueError("Test class order differs from saved labels.")

if len(dataset) == 0:
    raise ValueError("Test dataset is empty.")

loader = DataLoader(
    dataset, batch_size=BATCH_SIZE,
    shuffle=False, num_workers=0
)

print("Classes:", len(classes))
print("Test images:", len(dataset))
print("Loading model...")

model = models.efficientnet_b0(weights=None)
features = model.classifier[1].in_features
model.classifier = nn.Sequential(
    nn.Dropout(p=0.3),
    nn.Linear(features, 38)
)

state = torch.load(
    MODEL_PATH, map_location=device, weights_only=True
)
model.load_state_dict(state)
model.to(device)
model.eval()

# Per-class counts, with no SciPy or scikit-learn dependency.
class_total = [0] * 38
class_correct = [0] * 38
matrix = [[0] * 38 for _ in range(38)]
total = 0
correct = 0

print("Evaluating test images...")

with torch.no_grad():
    for batch_index, (images, labels) in enumerate(loader, 1):
        images = images.to(device)
        labels = labels.to(device)

        predictions = model(images).argmax(dim=1)

        total += labels.size(0)
        correct += (predictions == labels).sum().item()

        for actual, predicted in zip(
            labels.cpu().tolist(), predictions.cpu().tolist()
        ):
            class_total[actual] += 1
            matrix[actual][predicted] += 1
            if actual == predicted:
                class_correct[actual] += 1

        if batch_index % 20 == 0:
            print(f"Processed batch {batch_index}/{len(loader)}")

accuracy = 100.0 * correct / total

report_lines = [
    f"{'Class':55} {'Images':>7} {'Correct':>7} "
    f"{'Precision':>10} {'Recall':>10} {'F1-score':>10}"
]

macro_precision = 0.0
macro_recall = 0.0
macro_f1 = 0.0

for i, name in enumerate(classes):
    tp = matrix[i][i]
    predicted_total = sum(matrix[row][i] for row in range(38))
    actual_total = class_total[i]

    precision = tp / predicted_total if predicted_total else 0.0
    recall = tp / actual_total if actual_total else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0.0
    )

    macro_precision += precision
    macro_recall += recall
    macro_f1 += f1

    report_lines.append(
        f"{name:55.55} {actual_total:7d} {tp:7d} "
        f"{precision:10.4f} {recall:10.4f} {f1:10.4f}"
    )

macro_precision /= 38
macro_recall /= 38
macro_f1 /= 38

report_lines += [
    "",
    f"Macro precision: {macro_precision:.4f}",
    f"Macro recall:    {macro_recall:.4f}",
    f"Macro F1-score:  {macro_f1:.4f}",
    f"Test accuracy:   {accuracy:.2f}%"
]

results = {
    "model": "EfficientNet-B0",
    "number_of_classes": 38,
    "test_images": total,
    "correct": correct,
    "incorrect": total - correct,
    "test_accuracy_percent": round(accuracy, 2),
    "macro_precision": round(macro_precision, 4),
    "macro_recall": round(macro_recall, 4),
    "macro_f1_score": round(macro_f1, 4),
    "classes": classes,
    "per_class": {
        classes[i]: {
            "images": class_total[i],
            "correct": class_correct[i],
            "precision": round(
                matrix[i][i] / sum(matrix[row][i] for row in range(38)), 4
            ) if sum(matrix[row][i] for row in range(38)) else 0.0,
            "recall": round(
                class_correct[i] / class_total[i], 4
            ) if class_total[i] else 0.0
        }
        for i in range(38)
    },
    "confusion_matrix": matrix
}

with RESULT_PATH.open("w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

with REPORT_PATH.open("w", encoding="utf-8") as f:
    f.write("PLANTCARE AI - 38 CLASS TEST REPORT\n\n")
    f.write(f"Test images: {total}\n")
    f.write(f"Correct predictions: {correct}\n")
    f.write(f"Incorrect predictions: {total - correct}\n")
    f.write(f"Test accuracy: {accuracy:.2f}%\n\n")
    f.write("\n".join(report_lines))
    f.write("\n\nCONFUSION MATRIX (rows=actual, columns=predicted)\n")
    for row in matrix:
        f.write(str(row) + "\n")

print("\n" + "=" * 60)
print("TEST EVALUATION COMPLETE")
print("=" * 60)
print("Test images:", total)
print("Correct:", correct)
print("Incorrect:", total - correct)
print(f"TEST ACCURACY: {accuracy:.2f}%")
print(f"Macro F1-score: {macro_f1:.4f}")
print("\nClass-wise report:")
print("\n".join(report_lines))
print("\nSaved results:", RESULT_PATH)
print("Saved report:", REPORT_PATH)
