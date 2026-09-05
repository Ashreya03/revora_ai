import streamlit as st


# =========================================================
# PRIORITY COLORS
# =========================================================

PRIORITY_COLORS = {
    "High": "#F87171",
    "Medium": "#FBBF24",
    "Low": "#34D399",
}


# =========================================================
# GLOBAL STYLES
# =========================================================

def inject_global_styles():

    st.markdown(
        """
        <style>

        /* =================================================
           THEME VARIABLES
        ================================================= */

        :root {
            --revora-primary: var(--st-primary-color);
            --revora-bg: var(--st-background-color);
            --revora-surface: var(--st-secondary-background-color);
            --revora-text: var(--st-text-color);
            --revora-border: var(--st-border-color);

            --revora-purple: #8B5CF6;
            --revora-purple-light: #A78BFA;
            --revora-pink: #EC4899;

            --revora-green: #34D399;
            --revora-warning: #FBBF24;
            --revora-danger: #F87171;
        }


        /* =================================================
           MAIN APPLICATION
        ================================================= */

        .stApp {
            background: var(--revora-bg);
            color: var(--revora-text);
        }

        .main {
            color: var(--revora-text);
        }

        /* Make normal Streamlit text theme-aware */

        p,
        span,
        label,
        li {
            color: var(--revora-text);
        }


        /* =================================================
           HEADINGS
        ================================================= */

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: var(--revora-text) !important;
        }


        /* =================================================
           SIDEBAR
        ================================================= */

        section[data-testid="stSidebar"] {
            background: var(--revora-surface);
            border-right: 1px solid var(--revora-border);
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] div {
            color: var(--revora-text);
        }


        /* =================================================
           REVORA BRAND
        ================================================= */

        .revora-brand {
            padding: 10px 4px 24px 4px;
        }

        .revora-logo {
            width: 42px;
            height: 42px;

            border-radius: 12px;

            display: flex;
            align-items: center;
            justify-content: center;

            background: linear-gradient(
                135deg,
                #8B5CF6,
                #EC4899
            );

            color: #FFFFFF !important;

            font-size: 22px;
            font-weight: 800;
        }

        .revora-title {
            font-size: 21px;
            font-weight: 800;

            color: var(--revora-text) !important;
        }

        .revora-subtitle {
            font-size: 12px;

            color: var(--revora-text) !important;

            opacity: 0.65;
        }


        /* =================================================
           KPI CARDS
        ================================================= */

        .kpi-card {
            background: var(--revora-surface);

            border: 1px solid var(--revora-border);

            border-radius: 16px;

            padding: 20px;

            min-height: 120px;

            box-shadow:
                0 4px 16px rgba(0, 0, 0, 0.08);
        }

        .kpi-label {
            font-size: 13px;
            font-weight: 600;

            color: var(--revora-text) !important;

            opacity: 0.65;

            margin-bottom: 8px;
        }

        .kpi-value {
            font-size: 28px;
            font-weight: 800;

            color: var(--revora-text) !important;
        }

        .kpi-sub {
            font-size: 12px;

            color: var(--revora-text) !important;

            opacity: 0.6;

            margin-top: 6px;
        }


        /* =================================================
           GENERAL CARDS
        ================================================= */

        .card {
            background: var(--revora-surface);

            border: 1px solid var(--revora-border);

            border-radius: 16px;

            padding: 20px;

            color: var(--revora-text);
        }


        /* =================================================
           DATAFRAMES
        ================================================= */

        [data-testid="stDataFrame"] {
            border: 1px solid var(--revora-border);

            border-radius: 12px;
        }


        /* =================================================
           BUTTONS
        ================================================= */

        .stButton > button {
            border-radius: 10px;

            font-weight: 600;

            color: var(--revora-text);
        }


        /* =================================================
           TEXT INPUTS
        ================================================= */

        input,
        textarea {
            color: var(--revora-text) !important;

            background-color: var(--revora-surface) !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: var(--revora-text) !important;

            opacity: 0.5;
        }


        /* =================================================
           SELECTBOX / MULTISELECT
        ================================================= */

        [data-baseweb="select"] {
            color: var(--revora-text) !important;
        }

        [data-baseweb="select"] * {
            color: var(--revora-text) !important;
        }


        /* =================================================
           CHAT MESSAGES
        ================================================= */

        [data-testid="stChatMessage"] {
            color: var(--revora-text);
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] li {
            color: var(--revora-text) !important;
        }


        /* =================================================
           CHAT INPUT
        ================================================= */

        [data-testid="stChatInput"] {
            background: var(--revora-surface);
        }

        [data-testid="stChatInput"] textarea {
            color: var(--revora-text) !important;
        }


        /* =================================================
           ALERTS / INFO / SUCCESS / WARNING
        ================================================= */

        [data-testid="stAlert"] {
            color: var(--revora-text);
        }

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span {
            color: inherit;
        }


        /* =================================================
           METRICS
        ================================================= */

        [data-testid="stMetricLabel"] {
            color: var(--revora-text) !important;

            opacity: 0.7;
        }

        [data-testid="stMetricValue"] {
            color: var(--revora-text) !important;
        }

        [data-testid="stMetricDelta"] {
            color: var(--revora-text) !important;
        }


        /* =================================================
           LINKS
        ================================================= */

        a {
            color: var(--st-link-color, var(--revora-primary)) !important;
        }


        /* =================================================
           DIVIDERS
        ================================================= */

        hr {
            border-color: var(--revora-border);
        }


        /* =================================================
           CODE
        ================================================= */

        code {
            color: var(--st-code-text-color, var(--revora-text));
        }


        /* =================================================
           EXPANDERS
        ================================================= */

        [data-testid="stExpander"] {
            background: var(--revora-surface);

            border: 1px solid var(--revora-border);

            border-radius: 12px;
        }


        /* =================================================
           TABS
        ================================================= */

        button[data-baseweb="tab"] {
            color: var(--revora-text) !important;
        }


        /* =================================================
           FILE UPLOADERS
        ================================================= */

        [data-testid="stFileUploader"] {
            color: var(--revora-text);
        }


        /* =================================================
           MOBILE
        ================================================= */

        @media (max-width: 768px) {

            .kpi-card {
                padding: 16px;
            }

            .kpi-value {
                font-size: 24px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# TOP BAR
# =========================================================

def render_topbar():

    st.markdown(
        """
        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding:8px 0 20px 0;
        ">
            <div>
                <div style="
                    font-size:24px;
                    font-weight:800;
                    color:var(--st-text-color);
                ">
                    Revora AI
                </div>

                <div style="
                    font-size:12px;
                    color:var(--st-text-color);
                    opacity:0.65;
                ">
                    Revenue Recovery Intelligence
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )