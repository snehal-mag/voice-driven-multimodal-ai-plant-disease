import os
import shutil
import random

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOURCE_DIR = os.path.join(
    BASE_DIR,
    "PlantVillage-Dataset",
    "raw",
    "color"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "dataset"
)

# Number of images required for EACH class
IMAGES_PER_CLASS = 500

# Dataset split
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Reproducible random selection
RANDOM_SEED = 42

random.seed(RANDOM_SEED)


# ============================================================
# CLASS MAPPING
# ============================================================

CLASSES = {
    "Tomato_Yellow_Leaf_Curl_Virus":
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus",

    "Tomato_Bacterial_Spot":
        "Tomato___Bacterial_spot",

    "Tomato_Late_Blight":
        "Tomato___Late_blight",

    "Tomato_Septoria_Leaf_Spot":
        "Tomato___Septoria_leaf_spot",

    "Tomato_Healthy":
        "Tomato___healthy",

    "Pepper_Healthy":
        "Pepper,_bell___healthy",

    "Tomato_Target_Spot":
        "Tomato___Target_Spot",

    "Potato_Late_Blight":
        "Potato___Late_blight",
}


# ============================================================
# IMAGE EXTENSIONS
# ============================================================

VALID_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png"
}


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

print("=" * 70)
print("PLANT DISEASE DATASET PREPARATION")
print("=" * 70)

print("\nSource directory:")
print(SOURCE_DIR)

print("\nOutput directory:")
print(OUTPUT_DIR)

# Remove old dataset
if os.path.exists(OUTPUT_DIR):
    print("\nRemoving old dataset...")
    shutil.rmtree(OUTPUT_DIR)

# Create folders
for split in ["train", "validation", "test"]:
    os.makedirs(
        os.path.join(OUTPUT_DIR, split),
        exist_ok=True
    )


# ============================================================
# PROCESS EACH CLASS
# ============================================================

total_images = 0

print("\n" + "=" * 70)
print("PROCESSING CLASSES")
print("=" * 70)

for class_name, source_folder in CLASSES.items():

    source_path = os.path.join(
        SOURCE_DIR,
        source_folder
    )

    print(f"\nClass: {class_name}")
    print(f"Source: {source_folder}")

    # Check source folder
    if not os.path.exists(source_path):
        print("ERROR: Source folder does not exist!")
        raise FileNotFoundError(source_path)

    # Get images
    images = []

    for filename in os.listdir(source_path):

        file_path = os.path.join(
            source_path,
            filename
        )

        if os.path.isfile(file_path):

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension in VALID_EXTENSIONS:
                images.append(filename)

    print(f"Available images: {len(images)}")

    # Check minimum
    if len(images) < IMAGES_PER_CLASS:
        print(
            f"ERROR: Need {IMAGES_PER_CLASS} images "
            f"but only {len(images)} are available."
        )
        raise ValueError(
            f"Not enough images for {class_name}"
        )

    # Randomly select exactly 500
    random.shuffle(images)

    selected_images = images[:IMAGES_PER_CLASS]

    # Calculate split sizes
    train_count = int(
        IMAGES_PER_CLASS * TRAIN_RATIO
    )

    validation_count = int(
        IMAGES_PER_CLASS * VAL_RATIO
    )

    test_count = (
        IMAGES_PER_CLASS
        - train_count
        - validation_count
    )

    train_images = selected_images[
        :train_count
    ]

    validation_images = selected_images[
        train_count:
        train_count + validation_count
    ]

    test_images = selected_images[
        train_count + validation_count:
    ]

    # Create class folders
    train_class_dir = os.path.join(
        OUTPUT_DIR,
        "train",
        class_name
    )

    validation_class_dir = os.path.join(
        OUTPUT_DIR,
        "validation",
        class_name
    )

    test_class_dir = os.path.join(
        OUTPUT_DIR,
        "test",
        class_name
    )

    os.makedirs(
        train_class_dir,
        exist_ok=True
    )

    os.makedirs(
        validation_class_dir,
        exist_ok=True
    )

    os.makedirs(
        test_class_dir,
        exist_ok=True
    )

    # ========================================================
    # COPY TRAINING IMAGES
    # ========================================================

    for filename in train_images:

        source_file = os.path.join(
            source_path,
            filename
        )

        destination_file = os.path.join(
            train_class_dir,
            filename
        )

        shutil.copy2(
            source_file,
            destination_file
        )

    # ========================================================
    # COPY VALIDATION IMAGES
    # ========================================================

    for filename in validation_images:

        source_file = os.path.join(
            source_path,
            filename
        )

        destination_file = os.path.join(
            validation_class_dir,
            filename
        )

        shutil.copy2(
            source_file,
            destination_file
        )

    # ========================================================
    # COPY TEST IMAGES
    # ========================================================

    for filename in test_images:

        source_file = os.path.join(
            source_path,
            filename
        )

        destination_file = os.path.join(
            test_class_dir,
            filename
        )

        shutil.copy2(
            source_file,
            destination_file
        )

    print(
        f"Train      : {len(train_images)}"
    )

    print(
        f"Validation : {len(validation_images)}"
    )

    print(
        f"Test       : {len(test_images)}"
    )

    total_images += IMAGES_PER_CLASS


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("DATASET CREATION COMPLETED")
print("=" * 70)

print(f"\nTotal classes : {len(CLASSES)}")
print(f"Images/class  : {IMAGES_PER_CLASS}")
print(f"Total images  : {total_images}")

print("\nExpected dataset:")

print(
    f"Training   : {len(CLASSES) * 350} images"
)

print(
    f"Validation : {len(CLASSES) * 75} images"
)

print(
    f"Testing    : {len(CLASSES) * 75} images"
)

print(
    f"Total      : {len(CLASSES) * 500} images"
)

print("\nDataset location:")
print(OUTPUT_DIR)

print("\nClasses:")

for class_name in CLASSES:
    print(f"  - {class_name}")

print("\n" + "=" * 70)
print("READY FOR MODEL TRAINING")
print("=" * 70)