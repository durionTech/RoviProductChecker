from paddleocr import PaddleOCR
import os
import uuid


print("Loading PaddleOCR model...")

ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)

print("PaddleOCR model loaded successfully!")


def process_image(image_path):

    """
    Run PaddleOCR on one product image.

    Returns:
    - detected text
    - confidence scores
    - bounding box coordinates
    """

    try:

        result = ocr.predict(image_path)

        extracted_items = []
        full_text = []

        for res in result:

            texts = res.get("rec_texts", [])
            scores = res.get("rec_scores", [])
            boxes = res.get("rec_boxes", [])

            for index, text in enumerate(texts):

                score = 0

                if index < len(scores):
                    score = float(scores[index])

                box = None

                if index < len(boxes):

                    current_box = boxes[index]

                    box = [
                        int(value)
                        for value in current_box
                    ]

                extracted_items.append({
                    "text": text,
                    "confidence": round(score, 4),
                    "box": box
                })

                full_text.append(text)

        return {
            "success": True,
            "full_text": "\n".join(full_text),
            "items": extracted_items
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "full_text": "",
            "items": []
        }