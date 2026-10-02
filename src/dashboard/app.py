import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.dashboard.utils import get_data, get_model
from src.dashboard.styles import (
    inject_global_styles,
    render_header,
    render_metric_card,
    render_section_divider,
    get_plotly_layout,
)

st.set_page_config(
    page_title="Customer Intelligence Platform",
    page_icon="📊",
    layout="wide",
)

inject_global_styles()

render_header(
    "Customer Intelligence Platform",
    "Real-time churn analytics & predictive insights"
)

df = get_data()
model = get_model()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        render_metric_card("👥", "Total Customers", f"{len(df):,}", "fade-in-delay-1"),
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        render_metric_card("📉", "Overall Churn Rate", f"{df['churn'].mean()*100:.1f}%", "fade-in-delay-2"),
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        render_metric_card("⏳", "Avg. Tenure", f"{df['tenure'].mean():.0f} mo", "fade-in-delay-3"),
        unsafe_allow_html=True,
    )

render_section_divider()

# ── Charts ────────────────────────────────────────────────────────────────────
layout = get_plotly_layout()

col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="chart-container fade-in fade-in-delay-2">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Churn Rate by Contract Type</div>', unsafe_allow_html=True)

    contract_churn = df.groupby('contract')['churn'].mean() * 100
    fig1 = px.bar(
        contract_churn,
        labels={'value': 'Churn Rate (%)', 'contract': 'Contract Type'},
        color=contract_churn.index,
    )
    fig1.update_layout(**layout, showlegend=False)
    fig1.update_traces(
        marker_line_width=0,
        marker_cornerradius=8,
        hovertemplate="<b>%{x}</b><br>Churn Rate: %{y:.1f}%<extra></extra>",
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="chart-container fade-in fade-in-delay-3">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Churn Rate by Internet Service</div>', unsafe_allow_html=True)

    internet_churn = df.groupby('internet_service')['churn'].mean() * 100
    fig3 = px.bar(
        internet_churn,
        labels={'value': 'Churn Rate (%)', 'internet_service': 'Internet Service'},
        color=internet_churn.index,
    )
    fig3.update_layout(**layout, showlegend=False)
    fig3.update_traces(
        marker_line_width=0,
        marker_cornerradius=8,
        hovertemplate="<b>%{x}</b><br>Churn Rate: %{y:.1f}%<extra></extra>",
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

render_section_divider()

st.markdown('<div class="chart-container fade-in fade-in-delay-4">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Churn Rate by Tenure</div>', unsafe_allow_html=True)

# Bucket tenure into four meaningful lifecycle stages
df['tenure_bucket'] = pd.cut(
    df['tenure'],
    bins=[-1, 6, 12, 24, 100],
    labels=['0-6 months', '6-12 months', '1-2 years', '2+ years'],
)
tenure_churn = df.groupby('tenure_bucket')['churn'].mean() * 100
fig2 = px.bar(
    tenure_churn,
    labels={'value': 'Churn Rate (%)', 'tenure_bucket': 'Tenure'},
    color=tenure_churn.index,
)
fig2.update_layout(**layout, showlegend=False)
fig2.update_traces(
    marker_line_width=0,
    marker_cornerradius=8,
    hovertemplate="<b>%{x}</b><br>Churn Rate: %{y:.1f}%<extra></extra>",
)
st.plotly_chart(fig2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
