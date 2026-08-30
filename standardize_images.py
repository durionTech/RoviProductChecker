from PIL import Image
import os

# =====================================================
# PATHS
# =====================================================

INPUT_FOLDER = "processed_dataset/usable"

OUTPUT_FOLDER = "processed_dataset/standardized"


# =====================================================
# CREATE OUTPUT FOLDER
# =====================================================

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# =====================================================
# SUPPORTED INPUT FORMATS
# =====================================================

extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tiff",
    ".tif"
)


# =====================================================
# STATISTICS
# =====================================================

total_images = 0
converted_images = 0
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


    # Create product output folder
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

            image = Image.open(input_path)


            # -----------------------------------------
            # Convert image to RGB
            # -----------------------------------------

            if image.mode != "RGB":

                image = image.convert("RGB")


            # -----------------------------------------
            # Create output filename
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
            # Save as JPEG
            # -----------------------------------------

            image.save(
                output_path,
                "JPEG",
                quality=95
            )


            converted_images += 1

            print(
                f"✓ {filename} → {output_filename}"
            )


        except Exception as e:

            failed_images += 1

            print(
                f"✗ {filename} → ERROR: {e}"
            )


# =====================================================
# FINAL REPORT
# =====================================================

print()
print()
print("=" * 60)

print("IMAGE STANDARDIZATION COMPLETED")

print("=" * 60)

print(
    "Total Images      :",
    total_images
)

print(
    "Converted Images  :",
    converted_images
)

print(
    "Failed Images     :",
    failed_images
)

print("=" * 60)