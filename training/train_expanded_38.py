import json
import csv
import time
from pathlib import Path

import torch
from torch import nn, optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = ROOT / "expanded_38_dataset"
MODEL_DIR = ROOT / "model"

OLD_MODEL = MODEL_DIR / "combined_30_model_best.pth"
OLD_CLASSES = MODEL_DIR / "combined_30_classes.json"

NEW_MODEL = MODEL_DIR / "expanded_38_model_best.pth"
NEW_CLASSES = MODEL_DIR / "expanded_38_classes.json"
HISTORY = MODEL_DIR / "expanded_38_training_history.csv"

IMAGE_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 5
LEARNING_RATE = 0.0001

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

train_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

eval_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

train_data = datasets.ImageFolder(
    DATASET_DIR / "train",
    transform=train_transform
)

val_data = datasets.ImageFolder(
    DATASET_DIR / "validation",
    transform=eval_transform
)

classes = train_data.classes
assert len(classes) == 38, f"Expected 38 classes, found {len(classes)}"
assert val_data.classes == classes

old_classes = json.loads(OLD_CLASSES.read_text(encoding="utf-8"))
assert len(old_classes) == 30

train_loader = DataLoader(
    train_data, batch_size=BATCH_SIZE,
    shuffle=True, num_workers=0
)

val_loader = DataLoader(
    val_data, batch_size=BATCH_SIZE,
    shuffle=False, num_workers=0
)

print("=" * 65)
print("PLANTCARE AI - 38 CLASS TRAINING")
print("=" * 65)
print("Device:", DEVICE)
print("Training images:", len(train_data))
print("Validation images:", len(val_data))
print("Classes:", len(classes))
print("Epochs:", EPOCHS)

# Create the original 30-class architecture.
model = models.efficientnet_b0(weights=None)
in_features = model.classifier[1].in_features

model.classifier = nn.Sequential(
    nn.Dropout(p=0.3),
    nn.Linear(in_features, 30)
)

# Load trained 30-class weights.
state = torch.load(OLD_MODEL, map_location="cpu", weights_only=True)
model.load_state_dict(state)

# Preserve old classifier weights while expanding to 38 classes.
old_linear = model.classifier[1]

new_linear = nn.Linear(in_features, 38)

with torch.no_grad():
    for old_idx, name in enumerate(old_classes):
        new_idx = classes.index(name)
        new_linear.weight[new_idx].copy_(old_linear.weight[old_idx])
        new_linear.bias[new_idx].copy_(old_linear.bias[old_idx])

model.classifier[1] = new_linear

# First train only the expanded classifier.
for parameter in model.features.parameters():
    parameter.requires_grad = False

model = model.to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(
    model.classifier.parameters(),
    lr=LEARNING_RATE
)

history = []
best_accuracy = -1.0

# Save class names to a separate file.
NEW_CLASSES.write_text(
    json.dumps(classes, indent=4, ensure_ascii=False),
    encoding="utf-8"
)

for epoch in range(EPOCHS):
    start = time.time()
    model.train()

    train_correct = 0
    train_total = 0
    train_loss = 0.0

    for batch_number, (images, labels) in enumerate(train_loader, 1):
        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item() * images.size(0)
        train_correct += (outputs.argmax(1) == labels).sum().item()
        train_total += labels.size(0)

        if batch_number % 100 == 0:
            print(f"Epoch {epoch + 1}: batch {batch_number}/{len(train_loader)}", flush=True)

    model.eval()
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)
            val_correct += (outputs.argmax(1) == labels).sum().item()
            val_total += labels.size(0)

    train_accuracy = 100 * train_correct / train_total
    val_accuracy = 100 * val_correct / val_total

    history.append({
        "epoch": epoch + 1,
        "train_loss": train_loss / train_total,
        "train_accuracy": train_accuracy,
        "val_accuracy": val_accuracy
    })

    print(
        f"Epoch {epoch + 1}/{EPOCHS} | "
        f"Train: {train_accuracy:.2f}% | "
        f"Validation: {val_accuracy:.2f}% | "
        f"Time: {(time.time() - start) / 60:.1f} min",
        flush=True
    )

    if val_accuracy > best_accuracy:
        best_accuracy = val_accuracy
        torch.save(model.state_dict(), NEW_MODEL)
        print(f"Best model saved! Accuracy: {best_accuracy:.2f}%", flush=True)

with HISTORY.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "epoch", "train_loss",
            "train_accuracy", "val_accuracy"
        ]
    )
    writer.writeheader()
    writer.writerows(history)

print("\nTRAINING COMPLETE!")
print("Best validation accuracy:", round(best_accuracy, 2), "%")
print("Model:", NEW_MODEL)
print("Classes:", NEW_CLASSES)
