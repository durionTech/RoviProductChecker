from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Optional
import os
import uuid
import shutil
from field_extractor import extract_fields
from ocr_service import process_image
from rule_engine import validate_compliance
from evidence_service import build_evidence

app = FastAPI(
    title="Legal Metrology AI Inspection API",
    description="Product label OCR and compliance inspection API",
    version="1.0.0"
)


# ============================================================
# UPLOAD DIRECTORY
# ============================================================

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# ============================================================
# HOME API
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Legal Metrology AI Inspection API is running",
        "status": "active"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "ocr": "PaddleOCR loaded"
    }


# ============================================================
# INSPECT PRODUCT
# ============================================================

@app.post("/inspect")
async def inspect_product(

    front_image: UploadFile = File(...),

    back_image: Optional[UploadFile] = File(None),

    side_image: Optional[UploadFile] = File(None)

):

    # --------------------------------------------------------
    # Validate front image
    # --------------------------------------------------------

    if not front_image.content_type.startswith("image/"):

        raise HTTPException(
            status_code=400,
            detail="Front image must be an image file"
        )


    # --------------------------------------------------------
    # Create unique inspection ID
    # --------------------------------------------------------

    inspection_id = str(uuid.uuid4())


    inspection_folder = os.path.join(
        UPLOAD_DIR,
        inspection_id
    )

    os.makedirs(
        inspection_folder,
        exist_ok=True
    )


    # --------------------------------------------------------
    # Process all uploaded images
    # --------------------------------------------------------

    uploaded_images = {
        "front": front_image,
        "back": back_image,
        "side": side_image
    }


    image_results = {}


    for image_type, image_file in uploaded_images.items():

        if image_file is None:
            continue


        # Validate image
        if not image_file.content_type.startswith("image/"):

            continue


        # Get file extension
        extension = os.path.splitext(
            image_file.filename
        )[1]

        if not extension:

            extension = ".jpg"


        # Create save path
        file_path = os.path.join(
            inspection_folder,
            f"{image_type}{extension}"
        )


        # Save uploaded image
        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                image_file.file,
                buffer
            )


        # Run OCR
        ocr_result = process_image(
            file_path
        )


        image_results[image_type] = {
            "filename": image_file.filename,
            "ocr": ocr_result
        }


    # --------------------------------------------------------
    # Combine all OCR text
    # --------------------------------------------------------

    all_text = []


    for image_type, data in image_results.items():

        text = data["ocr"].get(
            "full_text",
            ""
        )

        if text:
            all_text.append(
                f"[{image_type.upper()}]\n{text}"
            )


    combined_text = "\n\n".join(all_text)
    # --------------------------------------------------------
# COMBINE ALL OCR ITEMS
# --------------------------------------------------------

    combined_items = []

    for image_type, data in image_results.items():

        ocr_items = data["ocr"].get(
        "items",
        []
       )
 
    for item in ocr_items:

        item["image_type"] = image_type

        combined_items.append(item)


# Create combined OCR result
        combined_ocr_result = {

    "full_text": combined_text,

    "items": combined_items
     }


# --------------------------------------------------------
# EXTRACT STRUCTURED FIELDS
# --------------------------------------------------------

    extracted_fields = extract_fields(
    combined_ocr_result
)

# --------------------------------------------------------
# VALIDATE LEGAL METROLOGY COMPLIANCE
# --------------------------------------------------------

    compliance_result = validate_compliance(extracted_fields)
    # --------------------------------------------------------
# BUILD VISUAL EVIDENCE
# --------------------------------------------------------

    evidence = build_evidence(
    extracted_fields,
    combined_items
   )
    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {

        "success": True,

        "inspection_id": inspection_id,

        "images_processed": list(
            image_results.keys()
        ),
        "combined_text": combined_text,
        "extracted_fields": extracted_fields,
        "compliance_result": compliance_result,
        "evidence": evidence,
        "image_results": image_results
    }