"""
Shared CSS styles and animations for the Customer Intelligence Dashboard.
"""

def inject_global_styles():
    """Inject global CSS with animations, hover effects, and transitions."""
    import streamlit as st

    st.markdown("""
    <style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ===== BASE STYLES ===== */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ===== ANIMATED GRADIENT HEADER ===== */
    .dashboard-header {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }

    .dashboard-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%);
        animation: pulseGlow 4s ease-in-out infinite;
    }

    .dashboard-header h1 {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 30px rgba(99,102,241,0.5);
    }

    .dashboard-header p {
        color: rgba(255,255,255,0.7);
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        position: relative;
        z-index: 1;
    }

    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes pulseGlow {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50%      { opacity: 1; transform: scale(1.1); }
    }

    /* ===== FADE-IN ANIMATION ===== */
    .fade-in {
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
    }

    .fade-in-delay-1 { animation-delay: 0.1s; }
    .fade-in-delay-2 { animation-delay: 0.2s; }
    .fade-in-delay-3 { animation-delay: 0.3s; }
    .fade-in-delay-4 { animation-delay: 0.4s; }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ===== GLASSMORPHISM METRIC CARDS ===== */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
        position: relative;
        overflow: hidden;
    }

    .metric-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.05),
            transparent
        );
        transition: left 0.5s ease;
    }

    .metric-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
        border-color: rgba(99, 102, 241, 0.4);
    }

    .metric-card:hover::after {
        left: 100%;
    }

    .metric-card .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }

    .metric-card .metric-label {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }

    .metric-card .metric-icon {
        font-size: 1.5rem;
        margin-bottom: 0.3rem;
    }

    /* ===== CHART CONTAINER ===== */
    .chart-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }

    .chart-container:hover {
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.1);
    }

    .chart-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 1rem;
        padding-left: 0.5rem;
        border-left: 3px solid #6366f1;
    }

    /* ===== SECTION DIVIDER ===== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent);
        margin: 2rem 0;
        border: none;
    }

    /* ===== PREDICTION RESULT CARDS ===== */
    .result-card {
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        animation: fadeInUp 0.5s ease-out forwards;
        position: relative;
        overflow: hidden;
    }

    .result-card.high-risk {
        background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(239,68,68,0.05));
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    .result-card.low-risk {
        background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(34,197,94,0.05));
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .result-card .result-label {
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .result-card.high-risk .result-label { color: #ef4444; }
    .result-card.low-risk .result-label  { color: #22c55e; }

    .result-card .result-value {
        font-size: 3rem;
        font-weight: 700;
    }

    .result-card.high-risk .result-value { color: #ef4444; }
    .result-card.low-risk .result-value  { color: #22c55e; }

    /* ===== CHURN PROBABILITY RING ===== */
    .prob-ring-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1.5rem 0;
    }

    .prob-ring {
        width: 180px;
        height: 180px;
        position: relative;
    }

    .prob-ring svg {
        transform: rotate(-90deg);
    }

    .prob-ring .ring-bg {
        fill: none;
        stroke: rgba(255,255,255,0.08);
        stroke-width: 10;
    }

    .prob-ring .ring-fill {
        fill: none;
        stroke-width: 10;
        stroke-linecap: round;
        stroke-dasharray: 440;
        animation: ringFill 1.5s ease-out forwards;
    }

    .prob-ring .ring-fill.high { stroke: #ef4444; }
    .prob-ring .ring-fill.low  { stroke: #22c55e; }
    .prob-ring .ring-fill.mid  { stroke: #f59e0b; }

    @keyframes ringFill {
        from { stroke-dashoffset: 440; }
    }

    .prob-ring .ring-label {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }

    .prob-ring .ring-label .pct {
        font-size: 2rem;
        font-weight: 700;
    }

    .prob-ring .ring-label .sub {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ===== BUTTON STYLES ===== */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ===== SLIDER STYLES ===== */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    }

    /* ===== SELECT BOX STYLES ===== */
    .stSelectbox > div > div {
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }

    .stSelectbox > div > div:hover {
        border-color: #6366f1 !important;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }

    /* ===== HIDE DEFAULT STREAMLIT ELEMENTS ===== */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


def render_header(title, subtitle=None):
    """Render an animated gradient header."""
    import streamlit as st

    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div class="dashboard-header">
        <h1>{title}</h1>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(icon, label, value, delay_class=""):
    """Return HTML for a glassmorphism metric card."""
    return f"""
    <div class="metric-card fade-in {delay_class}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """


def render_section_divider():
    """Render an animated gradient divider."""
    import streamlit as st
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


def render_churn_ring(probability):
    """Render an animated SVG probability ring."""
    pct = probability * 100
    offset = 440 - (440 * probability)

    if pct >= 50:
        color_class = "high"
        color = "#ef4444"
    elif pct >= 30:
        color_class = "mid"
        color = "#f59e0b"
    else:
        color_class = "low"
        color = "#22c55e"

    return f"""
    <div class="prob-ring-container">
        <div class="prob-ring">
            <svg width="180" height="180" viewBox="0 0 180 180">
                <circle class="ring-bg" cx="90" cy="90" r="70" />
                <circle class="ring-fill {color_class}" cx="90" cy="90" r="70"
                        style="stroke-dashoffset: {offset};" />
            </svg>
            <div class="ring-label">
                <div class="pct" style="color: {color};">{pct:.1f}%</div>
                <div class="sub">churn risk</div>
            </div>
        </div>
    </div>
    """


def render_result_card(probability):
    """Render the high/low risk result card."""
    pct = probability * 100
    if pct >= 50:
        risk_class = "high-risk"
        label = "&#9888;&#65039; High Risk of Churn"
    else:
        risk_class = "low-risk"
        label = "&#9989; Low Risk of Churn"

    return f"""
    <div class="result-card {risk_class}">
        <div class="result-label">{label}</div>
        <div class="result-value">{pct:.1f}%</div>
    </div>
    """


def get_plotly_layout():
    """Return a consistent dark Plotly layout with smooth animations."""
    return dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="rgba(255,255,255,0.8)"),
        title_font=dict(size=16, color="rgba(255,255,255,0.9)"),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            zerolinecolor="rgba(255,255,255,0.05)",
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            zerolinecolor="rgba(255,255,255,0.05)",
        ),
        colorway=["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd",
                   "#818cf8", "#6d28d9", "#7c3aed", "#5b21b6"],
        margin=dict(l=40, r=40, t=50, b=40),
        hoverlabel=dict(
            bgcolor="rgba(15,12,41,0.9)",
            font_size=13,
            font_family="Inter, sans-serif",
            bordercolor="rgba(99,102,241,0.5)",
        ),
    )
