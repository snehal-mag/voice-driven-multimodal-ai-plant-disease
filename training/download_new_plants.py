import shutil
import subprocess
import sys
from pathlib import Path


# ============================================================
# PlantDiseaseAI
# Copy 10 New Plant Classes from PlantVillage
# ============================================================

PROJECT_DIR = Path(r"C:\Users\HP\Desktop\PlantDiseaseAI")

SOURCE_DIR = (
    PROJECT_DIR
    / "new_plant_source"
    / "raw"
    / "color"
)

OUTPUT_DIR = PROJECT_DIR / "new_plant_dataset"


# ------------------------------------------------------------
# Plant name mapping
# ------------------------------------------------------------

PLANT_PREFIXES = {
    "Apple": "Apple___",
    "Blueberry": "Blueberry___",
    "Cherry": "Cherry_(including_sour)___",
    "Corn": "Corn_(maize)___",
    "Grape": "Grape___",
    "Orange": "Orange___",
    "Peach": "Peach___",
    "Raspberry": "Raspberry___",
    "Soybean": "Soybean___",
    "Strawberry": "Strawberry___",
}


# ------------------------------------------------------------
# Image extensions
# ------------------------------------------------------------

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".JPG",
    ".JPEG",
    ".PNG",
}


# ------------------------------------------------------------
# Copy images
# ------------------------------------------------------------

def copy_images():

    if not SOURCE_DIR.exists():

        print()
        print("ERROR: PlantVillage source folder not found:")
        print(SOURCE_DIR)
        sys.exit(1)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print("=" * 70)
    print("COPYING 10 NEW PLANTS")
    print("=" * 70)

    total_images = 0
    found_plants = set()

    source_folders = [
        folder
        for folder in SOURCE_DIR.iterdir()
        if folder.is_dir()
    ]

    for plant, prefix in PLANT_PREFIXES.items():

        plant_folders = [
            folder
            for folder in source_folders
            if folder.name.startswith(prefix)
        ]

        if not plant_folders:

            print()
            print("NOT FOUND:", plant)

            continue

        found_plants.add(plant)

        print()
        print("=" * 60)
        print(plant)
        print("=" * 60)

        for source_folder in plant_folders:

            destination_folder = (
                OUTPUT_DIR / source_folder.name
            )

            destination_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            image_files = [
                file
                for file in source_folder.iterdir()
                if file.is_file()
                and file.suffix.lower()
                in {".jpg", ".jpeg", ".png"}
            ]

            copied = 0

            for image_file in image_files:

                destination_file = (
                    destination_folder
                    / image_file.name
                )

                if not destination_file.exists():

                    shutil.copy2(
                        image_file,
                        destination_file
                    )

                    copied += 1

            print(
                f"{source_folder.name} -> "
                f"{len(image_files)} images "
                f"({copied} newly copied)"
            )

            total_images += len(image_files)

    print()
    print("=" * 70)
    print("COPY COMPLETE")
    print("=" * 70)

    print()
    print(
        "Plants found:",
        len(found_plants),
        "/",
        len(PLANT_PREFIXES)
    )

    print(
        "Total images:",
        total_images
    )

    print()
    print("Output:")
    print(OUTPUT_DIR)

    missing = [
        plant
        for plant in PLANT_PREFIXES
        if plant not in found_plants
    ]

    if missing:

        print()
        print("Missing plants:")

        for plant in missing:
            print("-", plant)

    else:

        print()
        print("SUCCESS!")
        print("All 10 plants were found.")

    print()
    print(
        "Your original 8-class dataset was NOT modified."
    )


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

if __name__ == "__main__":

    copy_images()