# ============================================================
# EVIDENCE MAPPING SERVICE
# ============================================================

def find_evidence(items, search_value):
    """
    Find the OCR item that contains the extracted value.

    Returns the exact:
    - OCR text
    - confidence
    - bounding box
    - image type
    """

    if not search_value:
        return None

    search_value = str(search_value).lower().strip()

    for item in items:

        text = str(
            item.get("text", "")
        ).lower().strip()

        # Check whether extracted value appears in OCR text
        if search_value in text or text in search_value:

            return {
                "found": True,

                "detected_text": item.get(
                    "text"
                ),

                "confidence": item.get(
                    "confidence"
                ),

                "box": item.get(
                    "box"
                ),

                "image_type": item.get(
                    "image_type"
                )
            }

    return {
        "found": False,

        "detected_text": None,

        "confidence": None,

        "box": None,

        "image_type": None
    }


# ============================================================
# BUILD EVIDENCE FOR ALL FIELDS
# ============================================================

def build_evidence(extracted_fields, combined_items):

    evidence = {}

    # --------------------------------------------------------
    # MRP
    # --------------------------------------------------------

    mrp_data = extracted_fields.get(
        "mrp",
        {}
    )

    evidence["mrp"] = find_evidence(
        combined_items,
        mrp_data.get("value")
    )


    # --------------------------------------------------------
    # NET QUANTITY
    # --------------------------------------------------------

    quantity_data = extracted_fields.get(
        "net_quantity",
        {}
    )

    quantity_value = quantity_data.get(
        "value"
    )

    quantity_unit = quantity_data.get(
        "unit"
    )

    # Example: 100 + g = "100 g"
    if quantity_value and quantity_unit:

        quantity_search = (
            f"{quantity_value} {quantity_unit}"
        )

    else:

        quantity_search = quantity_value


    evidence["net_quantity"] = find_evidence(
        combined_items,
        quantity_search
    )


    # --------------------------------------------------------
    # MANUFACTURER
    # --------------------------------------------------------

    manufacturer_data = extracted_fields.get(
        "manufacturer",
        {}
    )

    evidence["manufacturer"] = find_evidence(
        combined_items,
        manufacturer_data.get("value")
    )


    # --------------------------------------------------------
    # MANUFACTURE DATE
    # --------------------------------------------------------

    date_data = extracted_fields.get(
        "manufacture_date",
        {}
    )

    evidence["manufacture_date"] = find_evidence(
        combined_items,
        date_data.get("value")
    )


    return evidence