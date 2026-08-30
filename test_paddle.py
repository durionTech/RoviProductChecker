from paddleocr import PaddleOCR

print("Loading PaddleOCR...")

ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)

print("PaddleOCR loaded successfully!")

image_path = r"processed_dataset\resized\Americana Coconut Cookies\Americana Coconut Cookies (11).jpg"

print("\nRunning OCR...\n")

result = ocr.predict(image_path)

print("=" * 50)
print("DETECTED TEXT")
print("=" * 50)

for res in result:

    texts = res["rec_texts"]
    scores = res["rec_scores"]

    for text, score in zip(texts, scores):
        print(f"{text}  →  Confidence: {score:.2%}")

print("=" * 50)
print("OCR completed successfully!")