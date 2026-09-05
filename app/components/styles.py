import streamlit as st


# ============================================================
# REVORA AI COLORS
# ============================================================

COLORS = {
    "bg": "#0F0B1A",
    "surface": "#1C1730",
    "surface_alt": "#241E3D",
    "border": "#332B52",

    "primary": "#8B5CF6",
    "primary_light": "#A78BFA",

    "accent_pink": "#EC4899",
    "accent_green": "#34D399",

    "text_primary": "#F5F3FF",
    "text_secondary": "#9D94BF",

    "success": "#34D399",
    "warning": "#FBBF24",
    "danger": "#F87171",
}


# ============================================================
# PRIORITY COLORS
# ============================================================

PRIORITY_COLORS = {
    "High": COLORS["danger"],
    "Medium": COLORS["warning"],
    "Low": COLORS["success"],
}


# ============================================================
# GLOBAL STYLES
# ============================================================

def inject_global_styles():

    st.markdown(
        f"""
        <style>

        /* ====================================================
           MAIN APP
        ==================================================== */

        .stApp {{
            background-color: {COLORS["bg"]};
            color: {COLORS["text_primary"]};
        }}

        .block-container {{
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }}


        /* ====================================================
           SIDEBAR
        ==================================================== */

        [data-testid="stSidebar"] {{
            background-color: {COLORS["surface"]};
            border-right: 1px solid {COLORS["border"]};
        }}

        [data-testid="stSidebar"] * {{
            color: {COLORS["text_primary"]};
        }}


        /* ====================================================
           SIDEBAR BRAND
        ==================================================== */

        [data-testid="stSidebar"]::before {{
            content: "Revora AI";
            display: block;

            padding: 18px 20px 4px 20px;

            font-size: 22px;
            font-weight: 800;

            letter-spacing: -0.04em;

            color: {COLORS["text_primary"]};
        }}

        [data-testid="stSidebar"]::after {{
            content: "Revenue Recovery Intelligence";

            display: block;

            padding: 0 20px 18px 20px;

            font-size: 11px;

            color: {COLORS["text_secondary"]};

            letter-spacing: 0.01em;
        }}


        /* ====================================================
           TOP BRAND
        ==================================================== */

        .topbar {{
            display: flex;
            align-items: center;

            padding: 4px 4px 20px 4px;
        }}

        .brand-container {{
            display: flex;
            align-items: center;

            gap: 13px;
        }}

        .brand-logo {{
            width: 44px;
            height: 44px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 14px;

            background:
                linear-gradient(
                    135deg,
                    #8B5CF6 0%,
                    #EC4899 100%
                );

            color: white;

            position: relative;

            box-shadow:
                0 8px 26px rgba(139, 92, 246, 0.30);
        }}

        .brand-logo::before {{
            content: "R";

            font-size: 24px;
            font-weight: 900;

            color: white;

            line-height: 1;
        }}

        .brand-logo::after {{
            content: "";

            position: absolute;

            width: 7px;
            height: 7px;

            border-radius: 50%;

            background: white;

            right: 7px;
            top: 7px;

            box-shadow:
                0 0 0 3px rgba(255,255,255,0.15);
        }}


        /* ====================================================
           BRAND TEXT
        ==================================================== */

        .topbar-brand {{
            font-size: 24px;

            font-weight: 800;

            letter-spacing: -0.045em;

            color: {COLORS["text_primary"]};
        }}

        .topbar-brand .brand-highlight {{
            color: {COLORS["primary_light"]};
        }}

        .brand-tagline {{
            font-size: 11px;

            color: {COLORS["text_secondary"]};

            margin-top: 2px;
        }}


        /* ====================================================
           KPI CARDS
        ==================================================== */

        .kpi-card {{
            background: linear-gradient(
                145deg,
                {COLORS["surface_alt"]} 0%,
                {COLORS["surface"]} 100%
            );

            border: 1px solid {COLORS["border"]};

            border-radius: 20px;

            padding: 22px 24px;

            min-height: 125px;

            box-shadow:
                0 8px 30px rgba(0, 0, 0, 0.18);

            transition:
                transform 0.2s ease,
                border-color 0.2s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);

            border-color: {COLORS["primary"]};
        }}

        .kpi-label {{
            color: {COLORS["text_secondary"]};

            font-size: 12px;

            font-weight: 700;

            text-transform: uppercase;

            letter-spacing: 0.08em;

            margin-bottom: 10px;
        }}

        .kpi-value {{
            color: {COLORS["text_primary"]};

            font-size: 30px;

            font-weight: 800;

            line-height: 1.15;
        }}

        .kpi-sub {{
            color: {COLORS["text_secondary"]};

            font-size: 12px;

            margin-top: 7px;
        }}


        /* ====================================================
           HEADINGS
        ==================================================== */

        h1 {{
            font-weight: 800 !important;

            letter-spacing: -0.03em;
        }}

        h2,
        h3 {{
            font-weight: 700 !important;

            letter-spacing: -0.02em;
        }}


        /* ====================================================
           TABLE
        ==================================================== */

        [data-testid="stDataFrame"] {{
            border-radius: 18px;

            overflow: hidden;

            border: 1px solid {COLORS["border"]};
        }}


        /* ====================================================
           DIVIDERS
        ==================================================== */

        hr {{
            border-color: {COLORS["border"]};
        }}


        /* ====================================================
           INPUTS
        ==================================================== */

        [data-baseweb="input"],
        [data-baseweb="select"] {{
            border-radius: 12px;
        }}


        /* ====================================================
           BUTTONS
        ==================================================== */

        .stButton > button {{
            border-radius: 12px;

            font-weight: 600;
        }}


        /* ====================================================
           CHAT
        ==================================================== */

        [data-testid="stChatMessage"] {{
            border-radius: 16px;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# OPTIONAL TOP BAR
# ============================================================

def render_topbar(title: str = "Dashboard"):

    st.markdown(
        """
        <div class="topbar">

            <div class="brand-container">

                <div class="brand-logo">
                    R
                </div>

                <div>

                    <div class="topbar-brand">
                        Rev<span class="brand-highlight">ora AI</span>
                    </div>

                    <div class="brand-tagline">
                        Revenue Recovery Intelligence
                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )