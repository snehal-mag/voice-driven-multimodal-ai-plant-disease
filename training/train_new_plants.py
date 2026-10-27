import os
import json
import csv
import torch
from pathlib import Path

from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from torch import nn, optim


# ============================================================
# PlantDiseaseAI
# EfficientNet-B0 - 22 New Plant Classes
# ============================================================

PROJECT_DIR = Path(
    r"C:\Users\HP\Desktop\PlantDiseaseAI"
)

DATASET_DIR = (
    PROJECT_DIR /
    "new_plant_training_dataset"
)

MODEL_DIR = (
    PROJECT_DIR /
    "model"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Configuration
# ============================================================

IMAGE_SIZE = 224

BATCH_SIZE = 16

EPOCHS = 8

LEARNING_RATE = 0.0001

NUM_WORKERS = 0

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# ============================================================
# Print configuration
# ============================================================

print()
print("=" * 70)
print("NEW PLANT DISEASE MODEL TRAINING")
print("=" * 70)

print()
print("Device       :", DEVICE)
print("Image size   :", IMAGE_SIZE)
print("Batch size   :", BATCH_SIZE)
print("Epochs       :", EPOCHS)
print("Learning rate:", LEARNING_RATE)

print()
print("Dataset:")
print(DATASET_DIR)


# ============================================================
# Check dataset
# ============================================================

TRAIN_DIR = DATASET_DIR / "train"
VAL_DIR = DATASET_DIR / "validation"

if not TRAIN_DIR.exists():

    raise FileNotFoundError(
        f"Training dataset not found:\n{TRAIN_DIR}"
    )

if not VAL_DIR.exists():

    raise FileNotFoundError(
        f"Validation dataset not found:\n{VAL_DIR}"
    )


# ============================================================
# Image transformations
# ============================================================

train_transforms = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.RandomHorizontalFlip(
        p=0.5
    ),

    transforms.RandomVerticalFlip(
        p=0.2
    ),

    transforms.RandomRotation(
        15
    ),

    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2
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


val_transforms = transforms.Compose([

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
# Load datasets
# ============================================================

print()
print("Loading datasets...")


train_dataset = datasets.ImageFolder(
    str(TRAIN_DIR),
    transform=train_transforms
)


val_dataset = datasets.ImageFolder(
    str(VAL_DIR),
    transform=val_transforms
)


class_names = train_dataset.classes

num_classes = len(class_names)


print()
print("Number of classes :", num_classes)

print()
print("Classes:")

for index, name in enumerate(
    class_names
):

    print(
        f"{index:2}: {name}"
    )


print()
print(
    "Training images   :",
    len(train_dataset)
)

print(
    "Validation images :",
    len(val_dataset)
)


# ============================================================
# DataLoaders
# ============================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=NUM_WORKERS
)


val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS
)


# ============================================================
# Load pretrained EfficientNet-B0
# ============================================================

print()
print("=" * 70)
print("LOADING EFFICIENTNET-B0")
print("=" * 70)

print()
print(
    "Downloading/loading ImageNet pretrained weights..."
)

weights = (
    models.EfficientNet_B0_Weights.DEFAULT
)

model = models.efficientnet_b0(
    weights=weights
)


# ============================================================
# Freeze feature extractor
# ============================================================

for parameter in model.features.parameters():

    parameter.requires_grad = False


# ============================================================
# Unfreeze last feature blocks
# ============================================================

for parameter in model.features[-2:].parameters():

    parameter.requires_grad = True


# ============================================================
# Replace classifier
# ============================================================

input_features = (
    model.classifier[1].in_features
)

model.classifier = nn.Sequential(

    nn.Dropout(
        p=0.3
    ),

    nn.Linear(
        input_features,
        num_classes
    )
)


model = model.to(
    DEVICE
)


# ============================================================
# Loss
# ============================================================

criterion = nn.CrossEntropyLoss()


# ============================================================
# Optimizer
# ============================================================

trainable_parameters = [
    parameter
    for parameter in model.parameters()
    if parameter.requires_grad
]


optimizer = optim.Adam(
    trainable_parameters,
    lr=LEARNING_RATE
)


# ============================================================
# Learning-rate scheduler
# ============================================================

scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="max",
    factor=0.5,
    patience=1
)


# ============================================================
# Training history
# ============================================================

history = []

best_val_accuracy = 0.0


BEST_MODEL_PATH = (
    MODEL_DIR /
    "new_plant_model_best.pth"
)

FINAL_MODEL_PATH = (
    MODEL_DIR /
    "new_plant_model.pth"
)

CLASSES_PATH = (
    MODEL_DIR /
    "new_plant_classes.json"
)

HISTORY_PATH = (
    MODEL_DIR /
    "new_plant_training_history.csv"
)


# ============================================================
# Training loop
# ============================================================

for epoch in range(
    EPOCHS
):

    print()
    print("=" * 70)

    print(
        f"EPOCH {epoch + 1}/{EPOCHS}"
    )

    print("=" * 70)


    # --------------------------------------------------------
    # Training
    # --------------------------------------------------------

    model.train()

    train_correct = 0

    train_total = 0

    train_loss_total = 0.0


    for batch_index, (
        images,
        labels
    ) in enumerate(
        train_loader
    ):

        images = images.to(
            DEVICE
        )

        labels = labels.to(
            DEVICE
        )


        optimizer.zero_grad()


        outputs = model(
            images
        )


        loss = criterion(
            outputs,
            labels
        )


        loss.backward()

        optimizer.step()


        train_loss_total += (
            loss.item()
            * images.size(0)
        )


        predictions = torch.argmax(
            outputs,
            dim=1
        )


        train_correct += (
            (predictions == labels)
            .sum()
            .item()
        )


        train_total += (
            labels.size(0)
        )


        if (
            batch_index + 1
        ) % 50 == 0:

            print(
                f"Batch "
                f"{batch_index + 1}/"
                f"{len(train_loader)}"
            )


    train_loss = (
        train_loss_total
        / train_total
    )


    train_accuracy = (
        train_correct
        / train_total
        * 100
    )


    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    model.eval()

    val_correct = 0

    val_total = 0

    val_loss_total = 0.0


    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(
                DEVICE
            )

            labels = labels.to(
                DEVICE
            )


            outputs = model(
                images
            )


            loss = criterion(
                outputs,
                labels
            )


            val_loss_total += (
                loss.item()
                * images.size(0)
            )


            predictions = torch.argmax(
                outputs,
                dim=1
            )


            val_correct += (
                (predictions == labels)
                .sum()
                .item()
            )


            val_total += (
                labels.size(0)
            )


    val_loss = (
        val_loss_total
        / val_total
    )


    val_accuracy = (
        val_correct
        / val_total
        * 100
    )


    # --------------------------------------------------------
    # Scheduler
    # --------------------------------------------------------

    scheduler.step(
        val_accuracy
    )


    current_lr = (
        optimizer.param_groups[0]["lr"]
    )


    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------

    print()

    print(
        f"Train Loss     : {train_loss:.4f}"
    )

    print(
        f"Train Accuracy : {train_accuracy:.2f}%"
    )

    print(
        f"Val Loss       : {val_loss:.4f}"
    )

    print(
        f"Val Accuracy   : {val_accuracy:.2f}%"
    )

    print(
        f"Learning Rate  : {current_lr:.7f}"
    )


    # --------------------------------------------------------
    # Save best model
    # --------------------------------------------------------

    if val_accuracy > best_val_accuracy:

        best_val_accuracy = val_accuracy

        torch.save(
            model.state_dict(),
            BEST_MODEL_PATH
        )

        print()
        print(
            "NEW BEST MODEL SAVED!"
        )

        print(
            f"Best validation accuracy: "
            f"{best_val_accuracy:.2f}%"
        )


    # --------------------------------------------------------
    # History
    # --------------------------------------------------------

    history.append({

        "epoch":
            epoch + 1,

        "train_loss":
            train_loss,

        "train_accuracy":
            train_accuracy,

        "val_loss":
            val_loss,

        "val_accuracy":
            val_accuracy,

        "learning_rate":
            current_lr
    })


# ============================================================
# Save final model
# ============================================================

torch.save(
    model.state_dict(),
    FINAL_MODEL_PATH
)


# ============================================================
# Save class names
# ============================================================

with open(
    CLASSES_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        class_names,
        file,
        indent=4,
        ensure_ascii=False
    )


# ============================================================
# Save training history
# ============================================================

with open(
    HISTORY_PATH,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "epoch",
            "train_loss",
            "train_accuracy",
            "val_loss",
            "val_accuracy",
            "learning_rate"
        ]
    )

    writer.writeheader()

    writer.writerows(
        history
    )


# ============================================================
# Final output
# ============================================================

print()
print("=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)

print()
print(
    "Number of classes :",
    num_classes
)

print(
    "Best validation accuracy :",
    f"{best_val_accuracy:.2f}%"
)

print()
print("Best model:")
print(BEST_MODEL_PATH)

print()
print("Final model:")
print(FINAL_MODEL_PATH)

print()
print("Classes:")
print(CLASSES_PATH)

print()
print("Training history:")
print(HISTORY_PATH)

print()
print(
    "IMPORTANT:"
)

print(
    "Your original 8-class model was NOT modified."
)

print("=" * 70)