"""
FORD Score prediction engine.
"""

from config import RISK_LEVELS, SCORE_RATES


def compute_prediction(inputs: dict) -> dict:
    """
    Compute the FORD score (0-10 scale) from raw input values.

    Args:
        inputs: dict mapping variable name to its raw value.

    Returns:
        dict with keys:
            - score: final FORD score (0-10)
            - raw_score: pre-truncation value
            - nonhome_pct: per-score non-home discharge %
            - risk_label: risk level string
            - risk_color: color for display
            - risk_nonhome_pct: group-level non-home discharge %
            - components: list of per-component contribution dicts
    """
    age = float(inputs.get("age", 50))
    sex = inputs.get("sex", "Male")
    gcs = float(inputs.get("gcs", 15))
    sbp = float(inputs.get("sbp", 120))
    hr = float(inputs.get("hr", 75))
    rr = float(inputs.get("rr", 16))
    height_in = float(inputs.get("height_in", 68))
    weight_lb = float(inputs.get("weight_lb", 170))
    bmi = (weight_lb / (height_in ** 2)) * 703
    fracture_site = inputs.get("fracture_site", "Other")
    mechanism = inputs.get("mechanism", "Fall")
    transport = inputs.get("transport", "Ambulance/Air")
    insurance = inputs.get("insurance", "Self-pay")

    components = [
        {
            "label": "GCS Severe (\u2264 8)",
            "condition": "GCS \u2264 8",
            "met": gcs <= 8,
            "points": 6,
        },
        {
            "label": "Hip/Femur Fracture",
            "condition": "Fracture site is Hip/Femur or Both",
            "met": fracture_site in ("Hip/Femur", "Both"),
            "points": 5,
        },
        {
            "label": "Resp Rate Low (< 12)",
            "condition": "RR < 12",
            "met": rr < 12,
            "points": 5,
        },
        {
            "label": "Insurance: Medicare",
            "condition": "Insurance = Medicare",
            "met": insurance == "Medicare",
            "points": 4,
        },
        {
            "label": "SBP Hypotensive (< 90)",
            "condition": "SBP < 90",
            "met": sbp < 90,
            "points": 4,
        },
        {
            "label": "Insurance: Other",
            "condition": "Insurance = Other",
            "met": insurance == "Other",
            "points": 4,
        },
        {
            "label": "Age \u2265 75",
            "condition": "Age \u2265 75",
            "met": age >= 75,
            "points": 3,
        },
        {
            "label": "Axial Fracture (Spine/Rib/Pelvis)",
            "condition": "Fracture site is Axial or Both",
            "met": fracture_site in ("Axial (Spine/Rib/Pelvis)", "Both"),
            "points": 3,
        },
        {
            "label": "Insurance: Private",
            "condition": "Insurance = Private",
            "met": insurance == "Private",
            "points": 3,
        },
        {
            "label": "Insurance: Charity",
            "condition": "Insurance = Charity",
            "met": insurance == "Charity",
            "points": 3,
        },
        {
            "label": "GCS Moderate (9-12)",
            "condition": "9 \u2264 GCS \u2264 12",
            "met": 9 <= gcs <= 12,
            "points": 3,
        },
        {
            "label": "BMI \u2265 40 (Class III Obesity)",
            "condition": "BMI \u2265 40",
            "met": bmi >= 40,
            "points": 2,
        },
        {
            "label": "Age 65-74",
            "condition": "65 \u2264 Age \u2264 74",
            "met": 65 <= age <= 74,
            "points": 1,
        },
        {
            "label": "Female",
            "condition": "Sex = Female",
            "met": sex == "Female",
            "points": 1,
        },
        {
            "label": "Resp Rate High (> 20)",
            "condition": "RR > 20",
            "met": rr > 20,
            "points": 1,
        },
        {
            "label": "Heart Rate Tachycardic (\u2265 100)",
            "condition": "HR \u2265 100",
            "met": hr >= 100,
            "points": 1,
        },
        {
            "label": "Transport: Private Vehicle",
            "condition": "Transport = Private Vehicle",
            "met": transport == "Private Vehicle",
            "points": -2,
        },
        {
            "label": "Mechanism: Assault",
            "condition": "Mechanism = Assault",
            "met": mechanism == "Assault",
            "points": -3,
        },
        {
            "label": "Transport: Walk-in",
            "condition": "Transport = Walk-in",
            "met": transport == "Walk-in",
            "points": -4,
        },
    ]

    for comp in components:
        comp["value"] = comp["points"] if comp["met"] else 0

    raw_score = sum(c["value"] for c in components)
    score = max(0, min(10, raw_score))

    nonhome_pct = SCORE_RATES.get(score, 0.0)

    risk_label = ""
    risk_color = "green"
    risk_nonhome_pct = 0.0
    for level in RISK_LEVELS:
        if score <= level["max_score"]:
            risk_label = level["label"]
            risk_color = level["color"]
            risk_nonhome_pct = level["nonhome_rate"]
            break

    return {
        "score": score,
        "raw_score": raw_score,
        "nonhome_pct": nonhome_pct,
        "risk_label": risk_label,
        "risk_color": risk_color,
        "risk_nonhome_pct": risk_nonhome_pct,
        "components": components,
    }
