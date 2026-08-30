from PIL import Image
import os

# =====================================================
# PATHS
# =====================================================

INPUT_FOLDER = "processed_dataset/standardized"

OUTPUT_FOLDER = "processed_dataset/resized"


# =====================================================
# SETTINGS
# =====================================================

MAX_WIDTH = 1280
MAX_HEIGHT = 1280

JPEG_QUALITY = 95


# =====================================================
# CREATE OUTPUT FOLDER
# =====================================================

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# =====================================================
# SUPPORTED IMAGE FORMAT
# =====================================================

extensions = (
    ".jpg",
    ".jpeg",
    ".png"
)


# =====================================================
# STATISTICS
# =====================================================

total_images = 0
resized_images = 0
unchanged_images = 0
failed_images = 0


# =====================================================
# PROCESS PRODUCT FOLDERS
# =====================================================

for product_name in os.listdir(INPUT_FOLDER):

    product_path = os.path.join(
        INPUT_FOLDER,
        product_name
    )

    # Ignore files
    if not os.path.isdir(product_path):
        continue


    print()
    print("=" * 60)
    print("PRODUCT:", product_name)
    print("=" * 60)


    # Create output product folder

    output_product_folder = os.path.join(
        OUTPUT_FOLDER,
        product_name
    )

    os.makedirs(
        output_product_folder,
        exist_ok=True
    )


    # =================================================
    # PROCESS IMAGES
    # =================================================

    for filename in os.listdir(product_path):

        if not filename.lower().endswith(
            extensions
        ):
            continue


        input_path = os.path.join(
            product_path,
            filename
        )


        total_images += 1


        try:

            # -----------------------------------------
            # Open image
            # -----------------------------------------

            image = Image.open(
                input_path
            )


            # -----------------------------------------
            # Convert to RGB
            # -----------------------------------------

            if image.mode != "RGB":

                image = image.convert("RGB")


            original_width, original_height = image.size


            # -----------------------------------------
            # Calculate resize ratio
            # -----------------------------------------

            scale = min(
                MAX_WIDTH / original_width,
                MAX_HEIGHT / original_height,
                1
            )


            # -----------------------------------------
            # Calculate new dimensions
            # -----------------------------------------

            new_width = int(
                original_width * scale
            )

            new_height = int(
                original_height * scale
            )


            # -----------------------------------------
            # Resize only if necessary
            # -----------------------------------------

            if scale < 1:

                resized_image = image.resize(
                    (new_width, new_height),
                    Image.Resampling.LANCZOS
                )

                resized_images += 1

            else:

                # Image is already smaller than
                # 1280 × 1280

                resized_image = image

                unchanged_images += 1


            # -----------------------------------------
            # Output filename
            # -----------------------------------------

            base_name = os.path.splitext(
                filename
            )[0]

            output_filename = (
                base_name + ".jpg"
            )


            output_path = os.path.join(
                output_product_folder,
                output_filename
            )


            # -----------------------------------------
            # Save image
            # -----------------------------------------

            resized_image.save(
                output_path,
                "JPEG",
                quality=JPEG_QUALITY,
                optimize=True
            )


            print(
                f"✓ {filename}"
                f" | {original_width}x{original_height}"
                f" → {new_width}x{new_height}"
            )


        except Exception as e:

            failed_images += 1

            print(
                f"✗ {filename}"
                f" → ERROR: {e}"
            )


# =====================================================
# FINAL REPORT
# =====================================================

print()
print()
print("=" * 60)

print("IMAGE RESIZING COMPLETED")

print("=" * 60)

print(
    "Total Images       :",
    total_images
)

print(
    "Resized Images     :",
    resized_images
)

print(
    "Already Small      :",
    unchanged_images
)

print(
    "Failed Images      :",
    failed_images
)

print("=" * 60)