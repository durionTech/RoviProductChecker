import os
import cv2
from PIL import Image
from paddleocr import PaddleOCR

# =====================================================
# PATHS
# =====================================================

INPUT_FOLDER = "processed_dataset/resized"
OUTPUT_FOLDER = "processed_dataset/oriented"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# =====================================================
# OCR MODEL
# =====================================================

print("Loading PaddleOCR model...")

ocr = PaddleOCR(
    lang="en"
)


# =====================================================
# SUPPORTED FORMATS
# =====================================================

EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png"
)


# =====================================================
# ROTATE IMAGE
# =====================================================

def rotate_image(image, angle):

    if angle == 0:
        return image

    elif angle == 90:
        return cv2.rotate(
            image,
            cv2.ROTATE_90_CLOCKWISE
        )

    elif angle == 180:
        return cv2.rotate(
            image,
            cv2.ROTATE_180
        )

    elif angle == 270:
        return cv2.rotate(
            image,
            cv2.ROTATE_90_COUNTERCLOCKWISE
        )


# =====================================================
# OCR SCORE FOR EACH ORIENTATION
# =====================================================

def get_ocr_score(image):

    try:

        # Run OCR
        result = ocr.predict(image)

        total_confidence = 0
        text_count = 0

        # Read OCR result
        for res in result:

            # Get recognized texts
            if "rec_scores" in res:

                scores = res["rec_scores"]

                for score in scores:
                    total_confidence += float(score)
                    text_count += 1


        # No text found
        if text_count == 0:
            return 0


        # Average OCR confidence
        return total_confidence / text_count


    except Exception as e:

        print("OCR Error:", e)

        return 0


# =====================================================
# FIND BEST ORIENTATION
# =====================================================

def correct_orientation(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return None, 0


    angles = [0, 90, 180, 270]

    best_score = -1
    best_angle = 0
    best_image = image


    # ---------------------------------------------
    # Test all 4 orientations
    # ---------------------------------------------

    for angle in angles:

        rotated_image = rotate_image(
            image,
            angle
        )

        score = get_ocr_score(
            rotated_image
        )

        print(
            f"      Angle {angle}° "
            f"→ OCR Score: {score:.3f}"
        )


        # Keep best orientation
        if score > best_score:

            best_score = score
            best_angle = angle
            best_image = rotated_image


    return best_image, best_angle


# =====================================================
# STATISTICS
# =====================================================

total_images = 0
corrected_images = 0
failed_images = 0


# =====================================================
# PROCESS PRODUCT FOLDERS
# =====================================================

for product_name in os.listdir(INPUT_FOLDER):

    product_path = os.path.join(
        INPUT_FOLDER,
        product_name
    )

    if not os.path.isdir(product_path):
        continue


    print()
    print("=" * 65)
    print("PRODUCT:", product_name)
    print("=" * 65)


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
    # PROCESS EACH IMAGE
    # =================================================

    for filename in os.listdir(product_path):

        if not filename.lower().endswith(EXTENSIONS):
            continue


        total_images += 1

        image_path = os.path.join(
            product_path,
            filename
        )

        print()
        print(f"Processing: {filename}")


        try:

            # -----------------------------------------
            # Find correct orientation
            # -----------------------------------------

            corrected_image, angle = correct_orientation(
                image_path
            )


            if corrected_image is None:

                print("✗ Could not read image")

                failed_images += 1

                continue


            # -----------------------------------------
            # Save corrected image
            # -----------------------------------------

            output_path = os.path.join(
                output_product_folder,
                filename
            )


            cv2.imwrite(
                output_path,
                corrected_image
            )


            if angle != 0:

                corrected_images += 1

                print(
                    f"✓ CORRECTED → Rotated {angle}°"
                )

            else:

                print(
                    "✓ Already correctly oriented"
                )


        except Exception as e:

            failed_images += 1

            print(
                f"✗ ERROR → {e}"
            )


# =====================================================
# FINAL REPORT
# =====================================================

print()
print()
print("=" * 65)
print("ORIENTATION CORRECTION COMPLETED")
print("=" * 65)

print("Total Images      :", total_images)
print("Images Rotated    :", corrected_images)
print("Failed Images     :", failed_images)

print("=" * 65)