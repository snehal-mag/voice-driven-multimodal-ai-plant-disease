import json
import os
import random
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SOURCE = ROOT / "combined_training_dataset"
PLANTVILLAGE = ROOT / "PlantVillage-Dataset" / "raw" / "color"
DEST = ROOT / "expanded_38_dataset"

NEW_CLASSES = {
    "Pepper,_bell___Bacterial_spot": "Pepper_Bacterial_Spot",
    "Potato___Early_blight": "Potato_Early_Blight",
    "Potato___healthy": "Potato_Healthy",
    "Squash___Powdery_mildew": "Squash_Powdery_Mildew",
    "Tomato___Early_blight": "Tomato_Early_Blight",
    "Tomato___Leaf_Mold": "Tomato_Leaf_Mold",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Tomato_Spider_Mites",
    "Tomato___Tomato_mosaic_virus": "Tomato_Mosaic_Virus",
}

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

random.seed(42)

existing_classes = json.loads(
    (ROOT / "model" / "combined_30_classes.json").read_text(
        encoding="utf-8"
    )
)

assert len(existing_classes) == 30
assert not set(NEW_CLASSES.values()) & set(existing_classes)

if DEST.exists():
    raise RuntimeError(
        "expanded_38_dataset already exists. "
        "Stopping to avoid changing an existing dataset."
    )

for split in ["train", "validation", "test"]:
    for name in existing_classes:
        src = SOURCE / split / name
        dst = DEST / split / name

        if not src.is_dir():
            raise FileNotFoundError(src)

        dst.mkdir(parents=True, exist_ok=True)

        for file in src.iterdir():
            if file.is_file() and file.suffix.lower() in EXTENSIONS:
                shutil.copy2(file, dst / file.name)

print("Existing 30 classes copied.")

for source_name, target_name in NEW_CLASSES.items():
    source_dir = PLANTVILLAGE / source_name

    if not source_dir.is_dir():
        raise FileNotFoundError(source_dir)

    images = [
        p for p in source_dir.iterdir()
        if p.is_file() and p.suffix.lower() in EXTENSIONS
    ]

    random.shuffle(images)

    n = len(images)
    train_end = int(n * 0.70)
    val_end = int(n * 0.85)

    splits = {
        "train": images[:train_end],
        "validation": images[train_end:val_end],
        "test": images[val_end:],
    }

    for split, files in splits.items():
        destination = DEST / split / target_name
        destination.mkdir(parents=True, exist_ok=True)

        for file in files:
            shutil.copy2(file, destination / file.name)

    print(
        f"{target_name}: {n} images "
        f"(train={len(splits['train'])}, "
        f"validation={len(splits['validation'])}, "
        f"test={len(splits['test'])})"
    )

print("\nFINAL DATASET SUMMARY")

for split in ["train", "validation", "test"]:
    folder = DEST / split

    classes = [p for p in folder.iterdir() if p.is_dir()]

    images = sum(
        1
        for cls in classes
        for file in cls.iterdir()
        if file.suffix.lower() in EXTENSIONS
    )

    print(f"{split}: {len(classes)} classes, {images} images")

print("\n38-class dataset preparation completed!")
print("Original 30-class dataset and model were not modified.")

