import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from src.features.preprocess import load_data
import joblib


@st.cache_data
def get_data():
    """Load and cache the full customers DataFrame from PostgreSQL.

    cache_data serialises the result to disk — safe for DataFrames.
    """
    return load_data()


@st.cache_resource
def get_model():
    """Load and cache the XGBoost model in memory for the session.

    cache_resource holds the object in memory without re-pickling it —
    correct for non-serialisable ML model objects.
    """
    return joblib.load('models/xgb_model.pkl')
