import os
import json
import csv
import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRAIN_DIR = os.path.join(BASE_DIR, "dataset", "train")
VAL_DIR = os.path.join(BASE_DIR, "dataset", "validation")
MODEL_DIR = os.path.join(BASE_DIR, "model")

os.makedirs(MODEL_DIR, exist_ok=True)

IMAGE_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 8
LEARNING_RATE = 0.0001

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ============================================================
# PRINT HEADER
# ============================================================

print("=" * 70)
print("PLANT DISEASE MODEL - PRETRAINED EFFICIENTNET-B0")
print("=" * 70)

print(f"Device        : {DEVICE}")
print(f"Image size    : {IMAGE_SIZE}")
print(f"Batch size    : {BATCH_SIZE}")
print(f"Epochs        : {EPOCHS}")
print(f"Learning rate : {LEARNING_RATE}")

# ============================================================
# TRANSFORMS
# ============================================================

train_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(p=0.2),
    transforms.RandomRotation(15),
    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2
    ),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

val_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ============================================================
# DATASETS
# ============================================================

print("\nLoading datasets...")

train_dataset = datasets.ImageFolder(
    TRAIN_DIR,
    transform=train_transform
)

val_dataset = datasets.ImageFolder(
    VAL_DIR,
    transform=val_transform
)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

classes = train_dataset.classes
num_classes = len(classes)

print("\nDataset information")
print("-" * 70)
print(f"Training images   : {len(train_dataset)}")
print(f"Validation images : {len(val_dataset)}")
print(f"Number of classes : {num_classes}")

print("\nClasses:")
for i, class_name in enumerate(classes):
    print(f"{i}: {class_name}")

# ============================================================
# SAVE CLASSES
# ============================================================

classes_path = os.path.join(MODEL_DIR, "classes.json")

with open(classes_path, "w", encoding="utf-8") as f:
    json.dump(classes, f, indent=4)

# ============================================================
# MODEL
# ============================================================

print("\n" + "=" * 70)
print("Creating pretrained EfficientNet-B0...")
print("=" * 70)

try:
    weights = models.EfficientNet_B0_Weights.DEFAULT

    print("\nLoading ImageNet pretrained weights...")
    model = models.efficientnet_b0(weights=weights)

    print("Pretrained weights loaded successfully.")

except Exception as e:

    print("\nWARNING: Could not load pretrained weights.")
    print("Error:", e)

    print("\nFalling back to randomly initialized model.")
    model = models.efficientnet_b0(weights=None)

# ============================================================
# FINE-TUNING
# ============================================================

# Freeze the early feature layers
for param in model.features.parameters():
    param.requires_grad = False

# Unfreeze the final feature blocks
for param in model.features[-2:].parameters():
    param.requires_grad = True

# Replace classifier
in_features = model.classifier[1].in_features

model.classifier = nn.Sequential(
    nn.Dropout(p=0.3),
    nn.Linear(in_features, num_classes)
)

model = model.to(DEVICE)

# ============================================================
# LOSS + OPTIMIZER
# ============================================================

criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=LEARNING_RATE
)

scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="max",
    factor=0.5,
    patience=2
)

# ============================================================
# TRAINING HISTORY
# ============================================================

history = []

best_val_accuracy = 0.0
best_model_path = os.path.join(
    MODEL_DIR,
    "plant_disease_model_best.pth"
)

final_model_path = os.path.join(
    MODEL_DIR,
    "plant_disease_model.pth"
)

# ============================================================
# TRAINING LOOP
# ============================================================

for epoch in range(EPOCHS):

    print("\n" + "=" * 70)
    print(f"Epoch {epoch + 1}/{EPOCHS}")
    print("=" * 70)

    # --------------------------------------------------------
    # TRAIN
    # --------------------------------------------------------

    model.train()

    train_loss = 0.0
    train_correct = 0
    train_total = 0

    for images, labels in train_loader:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        train_loss += loss.item() * images.size(0)

        _, predictions = torch.max(outputs, 1)

        train_correct += (
            predictions == labels
        ).sum().item()

        train_total += labels.size(0)

    train_loss /= train_total

    train_accuracy = (
        train_correct / train_total
    ) * 100

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    model.eval()

    val_loss = 0.0
    val_correct = 0
    val_total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)

            loss = criterion(outputs, labels)

            val_loss += loss.item() * images.size(0)

            _, predictions = torch.max(outputs, 1)

            val_correct += (
                predictions == labels
            ).sum().item()

            val_total += labels.size(0)

    val_loss /= val_total

    val_accuracy = (
        val_correct / val_total
    ) * 100

    scheduler.step(val_accuracy)

    # --------------------------------------------------------
    # PRINT RESULTS
    # --------------------------------------------------------

    print(f"Train Loss      : {train_loss:.4f}")
    print(f"Train Accuracy  : {train_accuracy:.2f}%")
    print(f"Val Loss        : {val_loss:.4f}")
    print(f"Val Accuracy    : {val_accuracy:.2f}%")

    # --------------------------------------------------------
    # SAVE HISTORY
    # --------------------------------------------------------

    history.append({
        "epoch": epoch + 1,
        "train_loss": train_loss,
        "train_accuracy": train_accuracy,
        "val_loss": val_loss,
        "val_accuracy": val_accuracy
    })

    # --------------------------------------------------------
    # SAVE BEST MODEL
    # --------------------------------------------------------

    if val_accuracy > best_val_accuracy:

        best_val_accuracy = val_accuracy

        torch.save(
            model.state_dict(),
            best_model_path
        )

        print("\nBest model saved!")
        print(
            f"Best validation accuracy: "
            f"{best_val_accuracy:.2f}%"
        )

# ============================================================
# SAVE FINAL MODEL
# ============================================================

torch.save(
    model.state_dict(),
    final_model_path
)

# ============================================================
# SAVE HISTORY CSV
# ============================================================

history_csv = os.path.join(
    MODEL_DIR,
    "training_history.csv"
)

with open(
    history_csv,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "epoch",
            "train_loss",
            "train_accuracy",
            "val_loss",
            "val_accuracy"
        ]
    )

    writer.writeheader()
    writer.writerows(history)

# ============================================================
# SAVE HISTORY JSON
# ============================================================

history_json = os.path.join(
    MODEL_DIR,
    "training_history.json"
)

with open(
    history_json,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        history,
        f,
        indent=4
    )

# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("TRAINING COMPLETED")
print("=" * 70)

print(
    f"\nBest validation accuracy: "
    f"{best_val_accuracy:.2f}%"
)

print("\nFinal model:")
print(final_model_path)

print("\nBest model:")
print(best_model_path)

print("\nClasses file:")
print(classes_path)

print("\nTraining history:")
print(history_csv)

print("\n" + "=" * 70)
print("MODEL READY FOR TEST EVALUATION")
print("=" * 70)