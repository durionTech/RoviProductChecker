import cv2
import numpy as np
import os

# ============================================================
# IMAGE PATH
# ============================================================

image_path = r"processed_dataset\oriented\Americana Coconut Cookies\Americana Coconut Cookies (11).jpg"

# ============================================================
# OUTPUT PATH
# ============================================================

output_dir = r"processed_dataset\perspective_corrected\Americana Coconut Cookies"

os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(
    output_dir,
    "Americana Coconut Cookies (11)_corrected.jpg"
)


# ============================================================
# LOAD IMAGE
# ============================================================

image = cv2.imread(image_path)

if image is None:
    print("ERROR: Image not found!")
    print(image_path)
    exit()

original = image.copy()


# ============================================================
# CLICK 4 CORNERS
# ============================================================

points = []


def click_event(event, x, y, flags, param):

    global points, image

    if event == cv2.EVENT_LBUTTONDOWN:

        # Save clicked point
        points.append([x, y])

        # Draw circle
        cv2.circle(image, (x, y), 8, (0, 255, 0), -1)

        # Show point number
        cv2.putText(
            image,
            str(len(points)),
            (x + 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        cv2.imshow("Select 4 Corners", image)

        print(f"Point {len(points)}: ({x}, {y})")


# ============================================================
# SHOW IMAGE
# ============================================================

print("\nSelect the 4 corners of the biscuit wrapper.")
print("Click in this order:")
print("1 → Top Left")
print("2 → Top Right")
print("3 → Bottom Right")
print("4 → Bottom Left")
print("\nPress ESC after selecting 4 points.\n")

cv2.imshow("Select 4 Corners", image)

cv2.setMouseCallback(
    "Select 4 Corners",
    click_event
)

cv2.waitKey(0)

cv2.destroyAllWindows()


# ============================================================
# CHECK POINTS
# ============================================================

if len(points) != 4:

    print("\nERROR!")
    print("You must select exactly 4 points.")
    print(f"You selected: {len(points)} points")

    exit()


# ============================================================
# CONVERT POINTS
# ============================================================

src_points = np.float32(points)


# ============================================================
# CALCULATE OUTPUT SIZE
# ============================================================

top_width = np.linalg.norm(
    src_points[1] - src_points[0]
)

bottom_width = np.linalg.norm(
    src_points[2] - src_points[3]
)

left_height = np.linalg.norm(
    src_points[3] - src_points[0]
)

right_height = np.linalg.norm(
    src_points[2] - src_points[1]
)

max_width = int(
    max(top_width, bottom_width)
)

max_height = int(
    max(left_height, right_height)
)


# ============================================================
# DESTINATION POINTS
# ============================================================

dst_points = np.float32([
    [0, 0],
    [max_width - 1, 0],
    [max_width - 1, max_height - 1],
    [0, max_height - 1]
])


# ============================================================
# PERSPECTIVE TRANSFORMATION
# ============================================================

matrix = cv2.getPerspectiveTransform(
    src_points,
    dst_points
)

corrected_image = cv2.warpPerspective(
    original,
    matrix,
    (max_width, max_height)
)


# ============================================================
# SAVE CORRECTED IMAGE
# ============================================================

cv2.imwrite(
    output_path,
    corrected_image
)


# ============================================================
# DISPLAY RESULT
# ============================================================

cv2.imshow(
    "Original Image",
    original
)

cv2.imshow(
    "Perspective Corrected Image",
    corrected_image
)

print("\n✓ Perspective correction completed!")
print("✓ Saved to:")
print(output_path)

print(f"\nOutput Size: {max_width} x {max_height}")

cv2.waitKey(0)

cv2.destroyAllWindows()