import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import streamlit as st
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from src.dashboard.utils import get_data, get_model
from src.dashboard.styles import (
    inject_global_styles,
    render_header,
    render_metric_card,
    render_section_divider,
    get_plotly_layout,
)
from src.features.preprocess import clean_data, split_features_target, encode_features

inject_global_styles()

render_header(
    "Model Performance",
    "Evaluate model accuracy, precision & recall across thresholds"
)

df = get_data()
model = get_model()

# Reproduce the exact same preprocessing and split used during training
# so the test-set metrics shown here match the offline evaluation.
df_clean, customer_id = clean_data(df)
x, y = split_features_target(df_clean)
x_encoded = encode_features(x)

x_train, x_test, y_train, y_test = train_test_split(
    x_encoded, y, test_size=0.2, stratify=y, random_state=42
)

render_section_divider()

st.markdown('<div class="fade-in">', unsafe_allow_html=True)
# 0.35 was empirically chosen during exploration — it maximises churn recall
# while keeping precision at an acceptable level for retention campaigns.
threshold = st.slider("Decision threshold", 0.0, 1.0, 0.35)
st.markdown('</div>', unsafe_allow_html=True)

probs = model.predict_proba(x_test)[:, 1]
y_pred = (probs >= threshold)

# ── KPI Metrics ───────────────────────────────────────────────────────────────
report = classification_report(y_test, y_pred, output_dict=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        render_metric_card("🎯", "Accuracy", f"{report['accuracy']*100:.1f}%", "fade-in-delay-1"),
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        render_metric_card("🔍", "Recall (Churn)", f"{report['True']['recall']*100:.1f}%", "fade-in-delay-2"),
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        render_metric_card("✅", "Precision (Churn)", f"{report['True']['precision']*100:.1f}%", "fade-in-delay-3"),
        unsafe_allow_html=True,
    )

render_section_divider()

# ── Confusion Matrix ──────────────────────────────────────────────────────────
st.markdown('<div class="chart-container fade-in fade-in-delay-3">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Confusion Matrix</div>', unsafe_allow_html=True)

cm = confusion_matrix(y_test, y_pred)
layout = get_plotly_layout()

fig = go.Figure(data=go.Heatmap(
    z=cm,
    x=['Predicted No Churn', 'Predicted Churn'],
    y=['Actual No Churn', 'Actual Churn'],
    text=cm,
    texttemplate="%{text}",
    textfont=dict(size=18, color="white"),
    colorscale=[
        [0, "rgba(99,102,241,0.1)"],
        [1, "rgba(99,102,241,0.8)"],
    ],
    hovertemplate="%{y} vs %{x}<br>Count: %{z}<extra></extra>",
    showscale=False,
))
fig.update_layout(
    **layout,
    height=400,
    xaxis_title="Predicted",
    yaxis_title="Actual",
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Probability Distribution ──────────────────────────────────────────────────
# Overlapping histograms show how well the model separates the two classes;
# a good model has minimal overlap between the No Churn and Churn distributions.
st.markdown('<div class="chart-container fade-in fade-in-delay-4">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Predicted Probability Distribution</div>', unsafe_allow_html=True)

fig_hist = go.Figure()
fig_hist.add_trace(go.Histogram(
    x=probs[y_test == False],
    name="No Churn",
    marker_color="rgba(99,102,241,0.6)",
    nbinsx=40,
    hovertemplate="Probability: %{x:.2f}<br>Count: %{y}<extra>No Churn</extra>",
))
fig_hist.add_trace(go.Histogram(
    x=probs[y_test == True],
    name="Churn",
    marker_color="rgba(239,68,68,0.6)",
    nbinsx=40,
    hovertemplate="Probability: %{x:.2f}<br>Count: %{y}<extra>Churn</extra>",
))
fig_hist.add_vline(
    x=threshold, line_dash="dash", line_color="#f59e0b",
    annotation_text=f"Threshold: {threshold}",
    annotation_font_color="#f59e0b",
)
fig_hist.update_layout(
    **layout,
    barmode="overlay",
    xaxis_title="Predicted Churn Probability",
    yaxis_title="Count",
    height=350,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig_hist, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
