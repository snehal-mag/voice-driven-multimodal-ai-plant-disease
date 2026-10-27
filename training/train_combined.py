import os
import json
import csv

import torch
from torch import nn, optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATASET_DIR = os.path.join(
    BASE_DIR,
    "combined_training_dataset"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "model"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


BEST_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "combined_30_model_best.pth"
)

FINAL_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "combined_30_model.pth"
)

CLASSES_PATH = os.path.join(
    MODEL_DIR,
    "combined_30_classes.json"
)

HISTORY_PATH = os.path.join(
    MODEL_DIR,
    "combined_30_training_history.csv"
)


# ============================================================
# SETTINGS
# ============================================================

IMAGE_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 8
LEARNING_RATE = 0.0001

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("UNIFIED 30-CLASS PLANT DISEASE MODEL TRAINING")
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
# DATASET CHECK
# ============================================================

TRAIN_DIR = os.path.join(
    DATASET_DIR,
    "train"
)

VAL_DIR = os.path.join(
    DATASET_DIR,
    "validation"
)

TEST_DIR = os.path.join(
    DATASET_DIR,
    "test"
)

if not os.path.exists(TRAIN_DIR):

    raise FileNotFoundError(
        f"Training dataset not found:\n{TRAIN_DIR}"
    )

if not os.path.exists(VAL_DIR):

    raise FileNotFoundError(
        f"Validation dataset not found:\n{VAL_DIR}"
    )

if not os.path.exists(TEST_DIR):

    raise FileNotFoundError(
        f"Test dataset not found:\n{TEST_DIR}"
    )


# ============================================================
# TRANSFORMS
# ============================================================

train_transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.RandomHorizontalFlip(),

    transforms.RandomVerticalFlip(),

    transforms.RandomRotation(
        20
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


val_transform = transforms.Compose([

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
# LOAD DATASETS
# ============================================================

print()
print("Loading datasets...")

train_dataset = datasets.ImageFolder(
    TRAIN_DIR,
    transform=train_transform
)

val_dataset = datasets.ImageFolder(
    VAL_DIR,
    transform=val_transform
)

test_dataset = datasets.ImageFolder(
    TEST_DIR,
    transform=val_transform
)


# ============================================================
# CLASSES
# ============================================================

classes = train_dataset.classes

num_classes = len(classes)

print()
print("Number of classes :", num_classes)

print()
print("Classes:")

for index, class_name in enumerate(classes):

    print(
        f"{index:2d}: {class_name}"
    )


# ============================================================
# SAVE CLASSES
# ============================================================

with open(
    CLASSES_PATH,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        classes,
        f,
        indent=4,
        ensure_ascii=False
    )


# ============================================================
# DATALOADERS
# ============================================================

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

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)


print()
print("Training images   :", len(train_dataset))
print("Validation images :", len(val_dataset))
print("Test images       :", len(test_dataset))


# ============================================================
# MODEL
# ============================================================

print()
print("=" * 70)
print("LOADING EFFICIENTNET-B0")
print("=" * 70)

print()
print("Downloading/loading ImageNet pretrained weights...")


model = models.efficientnet_b0(
    weights=models.EfficientNet_B0_Weights.DEFAULT
)


# ============================================================
# FREEZE FEATURES
# ============================================================

for parameter in model.features.parameters():

    parameter.requires_grad = False


# ============================================================
# UNFREEZE LAST TWO BLOCKS
# ============================================================

for parameter in model.features[-2:].parameters():

    parameter.requires_grad = True


# ============================================================
# CLASSIFIER
# ============================================================

in_features = model.classifier[1].in_features

model.classifier = nn.Sequential(

    nn.Dropout(
        p=0.3
    ),

    nn.Linear(
        in_features,
        num_classes
    )
)


model = model.to(
    DEVICE
)


# ============================================================
# LOSS
# ============================================================

criterion = nn.CrossEntropyLoss()


# ============================================================
# OPTIMIZER
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
# SCHEDULER
# ============================================================

scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="max",
    factor=0.5,
    patience=1
)


# ============================================================
# HISTORY
# ============================================================

history = []

best_val_accuracy = 0.0


# ============================================================
# TRAINING LOOP
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
    # TRAIN
    # --------------------------------------------------------

    model.train()

    running_loss = 0.0

    correct = 0

    total = 0


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


        running_loss += (
            loss.item()
            * images.size(0)
        )


        predictions = torch.argmax(
            outputs,
            dim=1
        )


        correct += (
            predictions == labels
        ).sum().item()


        total += labels.size(0)


        if (
            batch_index + 1
        ) % 50 == 0:

            print(
                f"Batch "
                f"{batch_index + 1}/"
                f"{len(train_loader)}"
            )


    train_loss = (
        running_loss
        / total
    )

    train_accuracy = (
        correct
        / total
    ) * 100


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    model.eval()

    val_loss_total = 0.0

    val_correct = 0

    val_total = 0


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
                predictions == labels
            ).sum().item()


            val_total += labels.size(0)


    val_loss = (
        val_loss_total
        / val_total
    )


    val_accuracy = (
        val_correct
        / val_total
    ) * 100


    # --------------------------------------------------------
    # LEARNING RATE
    # --------------------------------------------------------

    scheduler.step(
        val_accuracy
    )


    current_lr = optimizer.param_groups[0][
        "lr"
    ]


    # --------------------------------------------------------
    # PRINT
    # --------------------------------------------------------

    print()

    print(
        f"Train Loss     : "
        f"{train_loss:.4f}"
    )

    print(
        f"Train Accuracy : "
        f"{train_accuracy:.2f}%"
    )

    print(
        f"Val Loss       : "
        f"{val_loss:.4f}"
    )

    print(
        f"Val Accuracy   : "
        f"{val_accuracy:.2f}%"
    )

    print(
        f"Learning Rate  : "
        f"{current_lr:.7f}"
    )


    # --------------------------------------------------------
    # SAVE HISTORY
    # --------------------------------------------------------

    history.append({

        "epoch": epoch + 1,

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


    # --------------------------------------------------------
    # BEST MODEL
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


# ============================================================
# SAVE FINAL MODEL
# ============================================================

torch.save(
    model.state_dict(),
    FINAL_MODEL_PATH
)


# ============================================================
# SAVE HISTORY CSV
# ============================================================

with open(
    HISTORY_PATH,
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
            "val_accuracy",
            "learning_rate"
        ]
    )

    writer.writeheader()

    writer.writerows(
        history
    )


# ============================================================
# COMPLETE
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
    f"Best validation accuracy : "
    f"{best_val_accuracy:.2f}%"
)

print()

print(
    "Best model:"
)

print(
    BEST_MODEL_PATH
)

print()

print(
    "Final model:"
)

print(
    FINAL_MODEL_PATH
)

print()

print(
    "Classes:"
)

print(
    CLASSES_PATH
)

print()

print(
    "Training history:"
)

print(
    HISTORY_PATH
)

print()

print(
    "Original 8-class model was NOT modified."
)

print(
    "Original 22-class model was NOT modified."
)

print("=" * 70)