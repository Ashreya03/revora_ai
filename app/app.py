import streamlit as st

from components.styles import inject_global_styles


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Revora AI",
    page_icon=":material/auto_awesome:",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLES
# ============================================================

inject_global_styles()


# ============================================================
# PAGES
# ============================================================

overview_page = st.Page(
    "views/overview.py",
    title="Overview",
    icon=":material/dashboard:",
    default=True,
)

customers_page = st.Page(
    "views/customers.py",
    title="Customers",
    icon=":material/group:",
)

decisions_page = st.Page(
    "views/decisions.py",
    title="Decision Center",
    icon=":material/checklist:",
)

analytics_page = st.Page(
    "views/analytics.py",
    title="Analytics",
    icon=":material/analytics:",
)

recovery_page = st.Page(
    "views/recovery.py",
    title="Recovery Center",
    icon=":material/payments:",
)

ai_page = st.Page(
    "views/ai_assistant.py",
    title="AI Assistant",
    icon=":material/smart_toy:",
)


# ============================================================
# NAVIGATION
# ============================================================

pg = st.navigation(
    [
        overview_page,
        customers_page,
        decisions_page,
        analytics_page,
        recovery_page,
        ai_page,
    ],
    position="sidebar",
    expanded=True,
)


# ============================================================
# RUN SELECTED PAGE
# ============================================================

pg.run()