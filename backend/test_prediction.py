import os

from predict import predict_image


PROJECT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


TEST_DIR = os.path.join(
    PROJECT_DIR,
    "dataset",
    "test"
)


# ============================================================
# FIND FIRST TEST IMAGE
# ============================================================

image_path = None

for root, folders, files in os.walk(TEST_DIR):

    for file in files:

        if file.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):

            image_path = os.path.join(
                root,
                file
            )

            break

    if image_path:
        break


# ============================================================
# TEST PREDICTION
# ============================================================

if image_path is None:

    print("No test image found.")

else:

    print()
    print("Testing image:")
    print(image_path)

    disease, confidence = predict_image(
        image_path
    )

    print()
    print("Prediction:")
    print("Disease:", disease)
    print(
        "Confidence:",
        f"{confidence:.2f}%"
    )