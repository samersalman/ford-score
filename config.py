"""
FORD Score - Variable definitions for the input form.
"""

MODEL_NAME = "FORD Score"

RISK_LEVELS = [
    {"max_score": 1, "label": "Low", "color": "green", "nonhome_rate": 1.2},
    {"max_score": 3, "label": "Low-Moderate", "color": "orange", "nonhome_rate": 3.1},
    {"max_score": 6, "label": "Moderate-High", "color": "orange", "nonhome_rate": 7.0},
    {"max_score": 10, "label": "High", "color": "red", "nonhome_rate": 26.4},
]

SCORE_RATES = {
    0: 0.7,
    1: 1.7,
    2: 2.8,
    3: 2.9,
    4: 3.9,
    5: 9.6,
    6: 9.3,
    7: 14.7,
    8: 18.0,
    9: 22.9,
    10: 44.8,
}

VARIABLES = [
    # --- Patient Demographics ---
    {
        "name": "age",
        "label": "Age (years)",
        "type": "continuous",
        "min": 18,
        "max": 110,
        "step": 1,
        "default": 50,
        "group": "Patient Demographics",
    },
    {
        "name": "sex",
        "label": "Sex",
        "type": "categorical",
        "options": ["Male", "Female"],
        "group": "Patient Demographics",
    },
    {
        "name": "bmi",
        "label": "BMI (kg/m\u00b2)",
        "type": "continuous",
        "min": 10.0,
        "max": 80.0,
        "step": 0.1,
        "default": 25.0,
        "group": "Patient Demographics",
    },
    # --- ED Vital Signs ---
    {
        "name": "gcs",
        "label": "Glasgow Coma Scale (3-15)",
        "type": "continuous",
        "min": 3,
        "max": 15,
        "step": 1,
        "default": 15,
        "group": "ED Vital Signs",
    },
    {
        "name": "sbp",
        "label": "Systolic Blood Pressure (mmHg)",
        "type": "continuous",
        "min": 40,
        "max": 260,
        "step": 1,
        "default": 120,
        "group": "ED Vital Signs",
    },
    {
        "name": "hr",
        "label": "Heart Rate (bpm)",
        "type": "continuous",
        "min": 20,
        "max": 220,
        "step": 1,
        "default": 75,
        "group": "ED Vital Signs",
    },
    {
        "name": "rr",
        "label": "Respiratory Rate (breaths/min)",
        "type": "continuous",
        "min": 4,
        "max": 50,
        "step": 1,
        "default": 16,
        "group": "ED Vital Signs",
    },
    # --- Injury Characteristics ---
    {
        "name": "fracture_site",
        "label": "Fracture Site",
        "type": "categorical",
        "options": ["Other", "Hip/Femur", "Axial (Spine/Rib/Pelvis)", "Both"],
        "group": "Injury Characteristics",
    },
    {
        "name": "mechanism",
        "label": "Mechanism of Injury",
        "type": "categorical",
        "options": ["Fall", "MVC", "Assault", "Other"],
        "group": "Injury Characteristics",
    },
    # --- Prehospital & Insurance ---
    {
        "name": "transport",
        "label": "Transport Mode",
        "type": "categorical",
        "options": ["Ambulance/Air", "Private Vehicle", "Walk-in", "Other"],
        "group": "Prehospital & Insurance",
    },
    {
        "name": "insurance",
        "label": "Insurance",
        "type": "categorical",
        "options": ["Self-pay", "Medicare", "Medicaid", "Private", "Charity", "Other"],
        "group": "Prehospital & Insurance",
    },
]
