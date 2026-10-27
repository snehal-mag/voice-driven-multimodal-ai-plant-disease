import os
import shutil
import random
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ORIGINAL_DATASET = BASE_DIR / "dataset"

NEW_DATASET = BASE_DIR / "new_plant_training_dataset"

COMBINED_DATASET = BASE_DIR / "combined_training_dataset"

SEED = 42

random.seed(SEED)


# ============================================================
# CLASS FOLDERS
# ============================================================

splits = [
    "train",
    "validation",
    "test"
]


# ============================================================
# START
# ============================================================

print("=" * 70)
print("COMBINED 30-CLASS DATASET PREPARATION")
print("=" * 70)

print()
print("Original dataset:")
print(ORIGINAL_DATASET)

print()
print("New plant dataset:")
print(NEW_DATASET)

print()
print("Combined output:")
print(COMBINED_DATASET)


# ============================================================
# CHECK DATASETS
# ============================================================

for split in splits:

    original_split = ORIGINAL_DATASET / split
    new_split = NEW_DATASET / split

    if not original_split.exists():

        raise FileNotFoundError(
            f"Original dataset split not found:\n"
            f"{original_split}"
        )

    if not new_split.exists():

        raise FileNotFoundError(
            f"New dataset split not found:\n"
            f"{new_split}"
        )


# ============================================================
# REMOVE OLD COMBINED DATASET
# ============================================================

if COMBINED_DATASET.exists():

    print()
    print("Removing previous combined dataset...")

    shutil.rmtree(
        COMBINED_DATASET
    )


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

for split in splits:

    (
        COMBINED_DATASET / split
    ).mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# COPY DATASET
# ============================================================

total_images = 0

all_classes = set()


for split in splits:

    print()
    print("=" * 70)
    print(f"PROCESSING {split.upper()}")
    print("=" * 70)

    original_split = (
        ORIGINAL_DATASET / split
    )

    new_split = (
        NEW_DATASET / split
    )

    combined_split = (
        COMBINED_DATASET / split
    )


    # --------------------------------------------------------
    # ORIGINAL 8 CLASSES
    # --------------------------------------------------------

    print()
    print("Original 8 classes")

    for class_dir in sorted(
        original_split.iterdir()
    ):

        if not class_dir.is_dir():
            continue

        class_name = class_dir.name

        destination = (
            combined_split / class_name
        )

        destination.mkdir(
            parents=True,
            exist_ok=True
        )

        files = [
            f
            for f in class_dir.iterdir()
            if f.is_file()
        ]

        print(
            f"{class_name} -> "
            f"{len(files)} images"
        )

        for file in files:

            shutil.copy2(
                file,
                destination / file.name
            )

        all_classes.add(
            class_name
        )

        total_images += len(files)


    # --------------------------------------------------------
    # NEW 22 CLASSES
    # --------------------------------------------------------

    print()
    print("New 22 classes")

    for class_dir in sorted(
        new_split.iterdir()
    ):

        if not class_dir.is_dir():
            continue

        class_name = class_dir.name

        destination = (
            combined_split / class_name
        )

        destination.mkdir(
            parents=True,
            exist_ok=True
        )

        files = [
            f
            for f in class_dir.iterdir()
            if f.is_file()
        ]

        print(
            f"{class_name} -> "
            f"{len(files)} images"
        )

        for file in files:

            shutil.copy2(
                file,
                destination / file.name
            )

        all_classes.add(
            class_name
        )

        total_images += len(files)


# ============================================================
# VERIFY CLASSES
# ============================================================

print()
print("=" * 70)
print("DATASET VERIFICATION")
print("=" * 70)

print()
print(
    "Total classes:",
    len(all_classes)
)

print()

for index, class_name in enumerate(
    sorted(all_classes),
    start=1
):

    print(
        f"{index:2d}. {class_name}"
    )


# ============================================================
# COUNT EACH SPLIT
# ============================================================

print()
print("=" * 70)
print("FINAL DATASET COUNTS")
print("=" * 70)

grand_total = 0

for split in splits:

    split_dir = (
        COMBINED_DATASET / split
    )

    count = 0

    for class_dir in split_dir.iterdir():

        if not class_dir.is_dir():
            continue

        count += len([
            f
            for f in class_dir.iterdir()
            if f.is_file()
        ])

    grand_total += count

    print(
        f"{split.capitalize():12s}: "
        f"{count}"
    )


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 70)
print("COMBINED DATASET COMPLETE")
print("=" * 70)

print()
print(
    "Number of classes:",
    len(all_classes)
)

print(
    "Total images:",
    grand_total
)

print()
print(
    "Dataset created at:"
)

print(
    COMBINED_DATASET
)

print()
print(
    "Original 8-class dataset was NOT modified."
)

print(
    "New 22-class dataset was NOT modified."
)

print("=" * 70)