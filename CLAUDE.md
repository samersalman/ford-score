# FORD Score App

Clinical bedside tool predicting non-home discharge risk in orthopedic trauma patients. Score range: 0–10.

## Running the App

- Install: `pip install -r requirements.txt`
- Run: `streamlit run app.py`

## Architecture

Three modules, strict separation of concerns:

| File | Role |
|------|------|
| `config.py` | Single source of truth — variable definitions, risk level tiers, per-score discharge rates |
| `prediction.py` | Scoring engine — 19 weighted clinical rules, `compute_prediction(inputs) -> dict` |
| `app.py` | Streamlit UI — grouped form, results display, risk table, component breakdown chart |

Data flow: **app.py** reads variable metadata from **config.py** to build the form, passes user inputs to **prediction.py**, and renders the returned score/risk/components.

## Key Conventions

- All scoring rules are hardcoded in `prediction.py` (no external model files)
- Variable metadata (labels, types, groups, constraints) lives in `config.py` `VARIABLES` list
- Risk levels defined in `config.py` `RISK_LEVELS` — 4 tiers: Low, Low-Moderate, Moderate-High, High
- UI uses `st.form` with grouped `st.expander` sections and 2-column layout
- Score clamped to [0, 10] regardless of raw sum
- No tests currently; verify changes by running the app locally

## Adding a New Predictor

1. Add variable metadata to `VARIABLES` in `config.py`
2. Add scoring rule(s) to the `components` list in `prediction.py:compute_prediction()`
3. The UI picks it up automatically from config
