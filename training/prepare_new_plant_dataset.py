import random
import shutil
from pathlib import Path


# ============================================================
# PlantDiseaseAI
# Prepare balanced dataset for 22 new PlantVillage classes
# ============================================================

PROJECT_DIR = Path(r"C:\Users\HP\Desktop\PlantDiseaseAI")

SOURCE_DIR = PROJECT_DIR / "new_plant_dataset"

OUTPUT_DIR = PROJECT_DIR / "new_plant_training_dataset"

IMAGES_PER_CLASS = 500

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

RANDOM_SEED = 42

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png"
}


# ============================================================
# Main
# ============================================================

def main():

    random.seed(RANDOM_SEED)

    print()
    print("=" * 70)
    print("NEW PLANT DATASET PREPARATION")
    print("=" * 70)

    print()
    print("Source:")
    print(SOURCE_DIR)

    print()
    print("Output:")
    print(OUTPUT_DIR)

    if not SOURCE_DIR.exists():

        print()
        print("ERROR: Source dataset not found.")
        print(SOURCE_DIR)

        return

    # --------------------------------------------------------
    # Find classes
    # --------------------------------------------------------

    class_dirs = sorted([
        folder
        for folder in SOURCE_DIR.iterdir()
        if folder.is_dir()
    ])

    if not class_dirs:

        print()
        print("ERROR: No classes found.")

        return

    print()
    print("Classes found:", len(class_dirs))

    for index, folder in enumerate(
        class_dirs,
        start=1
    ):

        print(
            f"{index:2}. {folder.name}"
        )

    # --------------------------------------------------------
    # Recreate output directory
    # --------------------------------------------------------

    if OUTPUT_DIR.exists():

        print()
        print("Removing old prepared dataset...")

        shutil.rmtree(OUTPUT_DIR)

    train_dir = OUTPUT_DIR / "train"
    val_dir = OUTPUT_DIR / "validation"
    test_dir = OUTPUT_DIR / "test"

    train_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    val_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    test_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Counters
    # --------------------------------------------------------

    total_train = 0
    total_val = 0
    total_test = 0

    print()
    print("=" * 70)
    print("CREATING BALANCED DATASET")
    print("=" * 70)

    # --------------------------------------------------------
    # Process each class
    # --------------------------------------------------------

    for class_dir in class_dirs:

        class_name = class_dir.name

        images = [
            file
            for file in class_dir.iterdir()
            if file.is_file()
            and file.suffix.lower()
            in IMAGE_EXTENSIONS
        ]

        # Randomize images
        random.shuffle(images)

        original_count = len(images)

        # ----------------------------------------------------
        # Select maximum 500
        # ----------------------------------------------------

        selected_images = images[
            :min(
                IMAGES_PER_CLASS,
                len(images)
            )
        ]

        selected_count = len(
            selected_images
        )

        # ----------------------------------------------------
        # Calculate split
        # ----------------------------------------------------

        train_count = int(
            selected_count * TRAIN_RATIO
        )

        val_count = int(
            selected_count * VAL_RATIO
        )

        test_count = (
            selected_count
            - train_count
            - val_count
        )

        train_images = selected_images[
            :train_count
        ]

        val_images = selected_images[
            train_count:
            train_count + val_count
        ]

        test_images = selected_images[
            train_count + val_count:
        ]

        # ----------------------------------------------------
        # Create folders
        # ----------------------------------------------------

        train_class_dir = (
            train_dir / class_name
        )

        val_class_dir = (
            val_dir / class_name
        )

        test_class_dir = (
            test_dir / class_name
        )

        train_class_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        val_class_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        test_class_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # ----------------------------------------------------
        # Copy training images
        # ----------------------------------------------------

        for image in train_images:

            shutil.copy2(
                image,
                train_class_dir / image.name
            )

        # ----------------------------------------------------
        # Copy validation images
        # ----------------------------------------------------

        for image in val_images:

            shutil.copy2(
                image,
                val_class_dir / image.name
            )

        # ----------------------------------------------------
        # Copy test images
        # ----------------------------------------------------

        for image in test_images:

            shutil.copy2(
                image,
                test_class_dir / image.name
            )

        total_train += len(
            train_images
        )

        total_val += len(
            val_images
        )

        total_test += len(
            test_images
        )

        print()
        print(class_name)

        print(
            "  Available :",
            original_count
        )

        print(
            "  Selected  :",
            selected_count
        )

        print(
            "  Train     :",
            len(train_images)
        )

        print(
            "  Validation:",
            len(val_images)
        )

        print(
            "  Test      :",
            len(test_images)
        )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    total_images = (
        total_train
        + total_val
        + total_test
    )

    print()
    print("=" * 70)
    print("DATASET PREPARATION COMPLETE")
    print("=" * 70)

    print()
    print("Number of classes :", len(class_dirs))

    print(
        "Images/class      : up to",
        IMAGES_PER_CLASS
    )

    print()
    print(
        "Training images   :",
        total_train
    )

    print(
        "Validation images :",
        total_val
    )

    print(
        "Testing images    :",
        total_test
    )

    print(
        "Total images      :",
        total_images
    )

    print()
    print("Dataset created at:")

    print(OUTPUT_DIR)

    print()
    print("Train:")
    print(train_dir)

    print()
    print("Validation:")
    print(val_dir)

    print()
    print("Test:")
    print(test_dir)

    print()
    print("Existing 8-class dataset was NOT modified.")

    print("=" * 70)


if __name__ == "__main__":

    main()