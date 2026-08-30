# ============================================================
# LEGAL METROLOGY COMPLIANCE RULE ENGINE
# ============================================================

def check_field(field_data, field_name, rule_name):
    """
    Check whether a mandatory field was found.
    """

    if field_data.get("found", False):

        return {
            "rule": rule_name,
            "field": field_name,
            "status": "PASS",
            "message": f"{field_name} is present"
        }

    return {
        "rule": rule_name,
        "field": field_name,
        "status": "FAIL",
        "message": f"{field_name} is missing"
    }


# ============================================================
# MAIN COMPLIANCE CHECK
# ============================================================

def validate_compliance(extracted_fields):
    """
    Validate OCR extracted information against the
    mandatory prototype compliance checks.
    """

    checks = []


    # --------------------------------------------------------
    # CHECK 1: MRP
    # --------------------------------------------------------

    checks.append(
        check_field(
            extracted_fields.get("mrp", {}),
            "MRP",
            "MRP Declaration"
        )
    )


    # --------------------------------------------------------
    # CHECK 2: NET QUANTITY
    # --------------------------------------------------------

    checks.append(
        check_field(
            extracted_fields.get("net_quantity", {}),
            "Net Quantity",
            "Net Quantity Declaration"
        )
    )


    # --------------------------------------------------------
    # CHECK 3: MANUFACTURER
    # --------------------------------------------------------

    checks.append(
        check_field(
            extracted_fields.get("manufacturer", {}),
            "Manufacturer",
            "Manufacturer Declaration"
        )
    )


    # --------------------------------------------------------
    # CHECK 4: MANUFACTURE / PACKING DATE
    # --------------------------------------------------------

    checks.append(
        check_field(
            extracted_fields.get("manufacture_date", {}),
            "Manufacture Date",
            "Date Declaration"
        )
    )


    # --------------------------------------------------------
    # CALCULATE RESULT
    # --------------------------------------------------------

    failed_checks = [
        check
        for check in checks
        if check["status"] == "FAIL"
    ]


    passed_checks = [
        check
        for check in checks
        if check["status"] == "PASS"
    ]


    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    if len(failed_checks) == 0:

        final_status = "COMPLIANT"

    else:

        final_status = "NON-COMPLIANT"


    # --------------------------------------------------------
    # RETURN FINAL RESULT
    # --------------------------------------------------------

    return {

        "final_status": final_status,

        "total_checks": len(checks),

        "passed": len(passed_checks),

        "failed": len(failed_checks),

        "checks": checks,

        "violations": failed_checks

    }