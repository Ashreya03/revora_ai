
import pandas as pd
import streamlit as st


@st.cache_data
def load_customer_risk_data() -> pd.DataFrame:
    """
    Loads the final customer risk & decision table produced by the
    modeling + decision engine pipeline (Phases 7-9).

    Returns one row per eligible customer (420 rows), containing:
    plan_tier, current_mrr, current_arr, churn_probability,
    revenue_at_risk, priority, recommended_action, and behavioral
    signals (satisfaction, tickets, escalation, usage, upgrade/downgrade).
    """
    df = pd.read_csv("data/processed/customer_risk_decisions.csv")
    return df