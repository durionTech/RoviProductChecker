import re


# ============================================================
# CONFIDENCE FILTER
# ============================================================

def get_clean_text(ocr_result, min_confidence=0.50):
    """
    Keep OCR text only when confidence is above the threshold.
    """

    clean_lines = []

    items = ocr_result.get("items", [])

    for item in items:

        text = item.get("text", "").strip()
        confidence = item.get("confidence", 0)

        if text and confidence >= min_confidence:
            clean_lines.append(text)

    return "\n".join(clean_lines)


# ============================================================
# MRP EXTRACTION
# ============================================================

def extract_mrp(text):
    """
    Extract Maximum Retail Price.

    Examples supported:
    MRP ₹10
    M.R.P. Rs. 20
    MRP: Rs 50.00
    ₹100
    Rs.100
    """

    patterns = [

        r'M\.?\s*R\.?\s*P\.?\s*[:\-]?\s*(?:₹|Rs\.?|INR)\s*(\d+(?:\.\d{1,2})?)',

        r'(?:MRP|M\.R\.P\.?)\s*[:\-]?\s*(\d+(?:\.\d{1,2})?)',

        r'₹\s*(\d+(?:\.\d{1,2})?)',

        r'Rs\.?\s*(\d+(?:\.\d{1,2})?)'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return {
                "value": match.group(1),
                "found": True
            }

    return {
        "value": None,
        "found": False
    }


# ============================================================
# NET QUANTITY EXTRACTION
# ============================================================

def extract_net_quantity(text):
    """
    Extract quantity.

    Examples:
    Net Wt 100 g
    Net Quantity: 200g
    500 g
    1 kg
    250 ml
    """

    patterns = [

        r'NET\s*(?:WT|WEIGHT|QUANTITY)?\.?\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(kg|g|gm|grams|ml|l|litre|litres)',

        r'NET\s*(?:WT|WEIGHT|QUANTITY)',

        r'(\d+(?:\.\d+)?)\s*(kg|g|gm|grams|ml|l|litre|litres)'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            # First pattern containing number + unit
            if len(match.groups()) >= 2:

                return {
                    "value": match.group(1),
                    "unit": match.group(2),
                    "found": True
                }

    return {
        "value": None,
        "unit": None,
        "found": False
    }


# ============================================================
# DATE EXTRACTION
# ============================================================

def extract_date(text):
    """
    Extract manufacturing / packing date.

    Examples:
    MFD: 08/2026
    PKD 12/2025
    MFG DATE: 01-2026
    PACKED ON: 08/2026
    """

    patterns = [

        r'(?:MFD|MFG|MANUFACTURED|MANUFACTURE\s*DATE|PKD|PACKED\s*ON)\s*[:\-]?\s*(\d{1,2}[/-]\d{2,4})',

        r'(?:MFD|MFG|MANUFACTURED|PKD)\s*[:\-]?\s*(\d{4}[/-]\d{1,2})'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return {
                "value": match.group(1),
                "found": True
            }

    return {
        "value": None,
        "found": False
    }


# ============================================================
# MANUFACTURER EXTRACTION
# ============================================================

def extract_manufacturer(text):
    """
    Find manufacturer/company information.
    """

    lines = text.split("\n")

    keywords = [
        "manufactured by",
        "manufacturer",
        "marketed by",
        "packed by",
        "mfg by"
    ]

    for index, line in enumerate(lines):

        lower_line = line.lower()

        for keyword in keywords:

            if keyword in lower_line:

                # Remove the keyword from the line
                company = re.sub(
                    keyword,
                    "",
                    line,
                    flags=re.IGNORECASE
                ).strip(" :-")

                # If name is on the same line
                if company:

                    return {
                        "value": company,
                        "found": True
                    }

                # Otherwise check next line
                if index + 1 < len(lines):

                    next_line = lines[index + 1].strip()

                    if next_line:

                        return {
                            "value": next_line,
                            "found": True
                        }

    return {
        "value": None,
        "found": False
    }


# ============================================================
# MAIN EXTRACTION FUNCTION
# ============================================================

def extract_fields(ocr_result):
    """
    Convert PaddleOCR output into structured product information.
    """

    clean_text = get_clean_text(
        ocr_result,
        min_confidence=0.50
    )

    return {

        "clean_text": clean_text,

        "mrp": extract_mrp(clean_text),

        "net_quantity": extract_net_quantity(clean_text),

        "manufacture_date": extract_date(clean_text),

        "manufacturer": extract_manufacturer(clean_text)

    }