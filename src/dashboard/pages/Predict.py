import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import streamlit as st
import pandas as pd
import joblib
from src.dashboard.utils import get_model
from src.dashboard.styles import (
    inject_global_styles,
    render_header,
    render_section_divider,
    render_churn_ring,
    render_result_card,
)

inject_global_styles()

render_header(
    "Predict Customer Churn",
    "Enter customer details to estimate churn probability"
)

model = get_model()
# model_columns ensures the sparse user-input DataFrame matches the full
# one-hot encoded feature space the model was trained on.
model_columns = joblib.load('models/model_columns.pkl')

render_section_divider()

# ── Input Form ────────────────────────────────────────────────────────────────
st.markdown('<div class="fade-in">', unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Contract & Service</div>', unsafe_allow_html=True)
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    payment_method = st.selectbox(
        "Payment Method",
        ["Electronic check", "Mailed check",
         "Bank transfer (automatic)", "Credit card (automatic)"],
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Usage Details</div>', unsafe_allow_html=True)
    tenure = st.slider("Tenure (months)", 0, 72, 12)
    monthly_charges = st.slider("Monthly Charges ($)", 18.0, 120.0, 70.0)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col_btn = st.columns([1, 1, 1])
with col_btn[1]:
    predict_clicked = st.button("🔮  Predict Churn Risk", use_container_width=True)

if predict_clicked:
    # Build a one-row DataFrame with only the features the user provided.
    # Missing one-hot columns are filled with 0 via reindex.
    input_df = pd.DataFrame([{
        'contract': contract,
        'tenure': tenure,
        'internet_service': internet_service,
        'monthly_charges': monthly_charges,
        'payment_method': payment_method,
    }])

    input_encoded = pd.get_dummies(input_df)
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

    probability = model.predict_proba(input_encoded)[:, 1][0]

    render_section_divider()

    # Animated SVG ring centred on page
    st.markdown(render_churn_ring(probability), unsafe_allow_html=True)

    col_res = st.columns([1, 2, 1])
    with col_res[1]:
        st.markdown(render_result_card(probability), unsafe_allow_html=True)

    # Only show retention suggestions for high-risk predictions to avoid
    # overwhelming analysts with noise on low-risk customers.
    if probability >= 0.5:
        st.markdown('<div class="chart-container fade-in fade-in-delay-2">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💡 Retention Suggestions</div>', unsafe_allow_html=True)

        suggestions = []
        if contract == "Month-to-month":
            suggestions.append("• Offer a discounted annual contract to increase commitment")
        if internet_service == "Fiber optic":
            suggestions.append("• Review fiber optic pricing — it correlates with higher churn")
        if payment_method == "Electronic check":
            suggestions.append("• Encourage switching to automatic payment for convenience")
        if tenure < 12:
            suggestions.append("• New customer — prioritize onboarding experience and early support")
        if monthly_charges > 80:
            suggestions.append("• High monthly charges — consider a loyalty discount or bundle")

        if not suggestions:
            suggestions.append("• Schedule a proactive outreach call to understand concerns")

        for s in suggestions:
            st.markdown(
                f"<p style='color:rgba(255,255,255,0.8); font-size:0.95rem; margin:0.3rem 0;'>{s}</p>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)
