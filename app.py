"""
Streamlit UI for the FORD Score app.
"""

import streamlit as st
import pandas as pd
from collections import OrderedDict
from config import VARIABLES, MODEL_NAME, RISK_LEVELS
from prediction import compute_prediction

st.set_page_config(page_title=MODEL_NAME, layout="wide")

st.title(MODEL_NAME)

with st.expander("About the FORD Score", expanded=False):
    st.markdown(
        "The **Fracture Orthopedic Risk of Discharge (FORD) Score** is a novel "
        "bedside predictive tool for non-home discharge in orthopedic trauma patients.\n\n"
        "It produces a score from **0–10** using patient demographics, ED vital signs, "
        "injury characteristics, and prehospital/insurance factors. Higher scores indicate "
        "greater risk of non-home discharge (e.g., rehab facility, skilled nursing).\n\n"
        "**How to use:** Fill in the fields below, click **Calculate**, and review the "
        "score, risk level, and component breakdown."
    )

# --- Build grouped variable structure ---
groups = OrderedDict()
for var in VARIABLES:
    group = var.get("group", "General")
    groups.setdefault(group, []).append(var)

# --- Input Form ---
inputs = {}

with st.form("prediction_form"):
    for group_name, group_vars in groups.items():
        with st.expander(group_name, expanded=True):
            cols = st.columns(2)
            for i, var in enumerate(group_vars):
                col = cols[i % 2]
                with col:
                    if var["type"] == "continuous":
                        inputs[var["name"]] = st.number_input(
                            var["label"],
                            min_value=float(var["min"]),
                            max_value=float(var["max"]),
                            value=float(var["default"]),
                            step=float(var["step"]),
                            key=var["name"],
                        )
                    elif var["type"] == "categorical":
                        selected = st.selectbox(
                            var["label"],
                            options=var["options"],
                            key=var["name"],
                        )
                        inputs[var["name"]] = selected

    submitted = st.form_submit_button("Calculate", type="primary", use_container_width=True)

# --- Results ---
if submitted:
    result = compute_prediction(inputs)
    score = result["score"]

    st.divider()
    st.subheader("Result")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="FORD Score (0-10)", value=f"{score}")
    with col2:
        st.markdown(f"### :{result['risk_color']}[{result['risk_label']}]")
    with col3:
        st.metric(label="Non-Home Discharge Risk", value=f"{result['nonhome_pct']}%")

    # --- Risk level reference table ---
    st.subheader("Risk Level Reference")
    ref_rows = []
    prev_max = -1
    for level in RISK_LEVELS:
        low = prev_max + 1
        high = level["max_score"]
        if low == high:
            score_range = str(low)
        else:
            score_range = f"{low}\u2013{high}"
        ref_rows.append({
            "FORD Score": score_range,
            "Risk Level": level["label"],
            "Non-Home Discharge Rate": f"{level['nonhome_rate']}%",
        })
        prev_max = high
    ref_df = pd.DataFrame(ref_rows)

    def highlight_current(row):
        if row["Risk Level"] == result["risk_label"]:
            return ["background-color: #d4edda; color: #155724"] * len(row)
        return [""] * len(row)

    st.dataframe(
        ref_df.style.apply(highlight_current, axis=1),
        use_container_width=True,
        hide_index=True,
    )

    # --- Component Breakdown ---
    st.subheader("Component Breakdown")

    components = result["components"]
    rows = []
    for c in components:
        rows.append({
            "Predictor": c["label"],
            "Condition": c["condition"],
            "Met?": "Yes" if c["met"] else "No",
            "Points": c["value"],
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- Bar chart of active components ---
    st.subheader("Active Components")
    active = [c for c in components if c["met"]]
    if active:
        chart_df = pd.DataFrame({
            "Component": [c["label"] for c in active],
            "Points": [c["points"] for c in active],
        })
        chart_df = chart_df.sort_values("Points", key=abs, ascending=True)
        chart_df = chart_df.set_index("Component")
        st.bar_chart(chart_df, horizontal=True)
    else:
        st.info("No risk factors are present with the current inputs.")
