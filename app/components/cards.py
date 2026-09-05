import streamlit as st


def kpi_card(label: str, value: str, sub: str = ""):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def priority_badge(priority: str, colors: dict) -> str:
    color = colors.get(priority, "#9AA0AC")
    return f'<span class="badge" style="background-color:{color}22; color:{color};">{priority}</span>'