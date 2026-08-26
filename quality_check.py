import cv2
import os
import shutil
import numpy as np

# =====================================================
# DATASET PATH
# =====================================================

INPUT_FOLDER = "datasets"
OUTPUT_FOLDER = "processed_dataset"

USABLE_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "usable"
)

REJECTED_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "rejected"
)


# =====================================================
# CREATE OUTPUT FOLDERS
# =====================================================

os.makedirs(USABLE_FOLDER, exist_ok=True)
os.makedirs(REJECTED_FOLDER, exist_ok=True)


# =====================================================
# SETTINGS
# =====================================================

BLUR_THRESHOLD = 50

DARK_THRESHOLD = 25

BRIGHT_THRESHOLD = 250

MIN_WIDTH = 300

MIN_HEIGHT = 300


# =====================================================
# IMAGE QUALITY FUNCTION
# =====================================================

def check_image(image_path):

    image = cv2.imread(image_path)

    # ---------------------------------------------
    # Check if image can be opened
    # ---------------------------------------------

    if image is None:
        return False, "corrupted_image"


    # ---------------------------------------------
    # Get image dimensions
    # ---------------------------------------------

    height, width = image.shape[:2]

    if width < MIN_WIDTH or height < MIN_HEIGHT:
        return False, "low_resolution"


    # ---------------------------------------------
    # Convert to grayscale
    # ---------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # ---------------------------------------------
    # Blur detection
    # ---------------------------------------------

    blur_score = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()


    if blur_score < BLUR_THRESHOLD:
        return False, "too_blurry"


    # ---------------------------------------------
    # Brightness detection
    # ---------------------------------------------

    brightness = np.mean(gray)


    if brightness < DARK_THRESHOLD:
        return False, "too_dark"


    if brightness > BRIGHT_THRESHOLD:
        return False, "overexposed"


    # ---------------------------------------------
    # Image is usable
    # ---------------------------------------------

    return True, "usable"


# =====================================================
# SUPPORTED IMAGE TYPES
# =====================================================

extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp"
)


# =====================================================
# STATISTICS
# =====================================================

total_images = 0

usable_images = 0

rejected_images = 0


# =====================================================
# PROCESS PRODUCT FOLDERS
# =====================================================

for product_name in os.listdir(INPUT_FOLDER):

    product_path = os.path.join(
        INPUT_FOLDER,
        product_name
    )


    # ---------------------------------------------
    # Ignore files
    # ---------------------------------------------

    if not os.path.isdir(product_path):
        continue


    print()
    print("=" * 60)

    print(
        "PRODUCT:",
        product_name
    )

    print("=" * 60)


    # ---------------------------------------------
    # Create product output folders
    # ---------------------------------------------

    usable_product_folder = os.path.join(
        USABLE_FOLDER,
        product_name
    )

    rejected_product_folder = os.path.join(
        REJECTED_FOLDER,
        product_name
    )


    os.makedirs(
        usable_product_folder,
        exist_ok=True
    )

    os.makedirs(
        rejected_product_folder,
        exist_ok=True
    )


    # ---------------------------------------------
    # Process images
    # ---------------------------------------------

    for filename in os.listdir(product_path):

        if not filename.lower().endswith(
            extensions
        ):
            continue


        image_path = os.path.join(
            product_path,
            filename
        )


        total_images += 1


        # -----------------------------------------
        # Quality check
        # -----------------------------------------

        is_usable, reason = check_image(
            image_path
        )


        # -----------------------------------------
        # Copy usable images
        # -----------------------------------------

        if is_usable:

            destination = os.path.join(
                usable_product_folder,
                filename
            )

            shutil.copy2(
                image_path,
                destination
            )

            usable_images += 1

            print(
                f"✓ {filename} → USABLE"
            )


        # -----------------------------------------
        # Copy rejected images
        # -----------------------------------------

        else:

            destination = os.path.join(
                rejected_product_folder,
                filename
            )

            shutil.copy2(
                image_path,
                destination
            )

            rejected_images += 1

            print(
                f"✗ {filename} → {reason}"
            )


# =====================================================
# FINAL REPORT
# =====================================================

print()
print()
print("=" * 60)

print("IMAGE QUALITY CHECK COMPLETED")

print("=" * 60)

print(
    "Total Images    :",
    total_images
)

print(
    "Usable Images   :",
    usable_images
)

print(
    "Rejected Images :",
    rejected_images
)

print("=" * 60)