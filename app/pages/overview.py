import streamlit as st
from data_loader import load_customer_risk_data
from components.styles import PRIORITY_COLORS
from components.cards import kpi_card, priority_badge

df = load_customer_risk_data()

st.title("Overview")

# --- KPI Row ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Total Customers", f"{len(df)}")

with col2:
    total_revenue_at_risk = df["revenue_at_risk"].sum()
    kpi_card("Revenue at Risk", f"${total_revenue_at_risk:,.0f}")

with col3:
    high_priority_count = (df["priority"] == "High").sum()
    kpi_card("High Priority Customers", f"{high_priority_count}")

with col4:
    avg_churn_prob = df["churn_probability"].mean()
    kpi_card("Avg Churn Probability", f"{avg_churn_prob:.1%}")

st.divider()

# --- Charts Row ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Customer Priority Distribution")
    priority_counts = df["priority"].value_counts()
    st.bar_chart(priority_counts)

with chart_col2:
    st.subheader("Revenue at Risk by Priority")
    revenue_by_priority = df.groupby("priority")["revenue_at_risk"].sum()
    st.bar_chart(revenue_by_priority)

st.divider()

# --- Top Customers Table ---
st.subheader("Top Customers by Revenue at Risk")
top_customers = df.sort_values("revenue_at_risk", ascending=False).head(10)
st.dataframe(
    top_customers[["account_id", "plan_tier", "churn_probability", "revenue_at_risk", "priority", "recommended_action"]],
    use_container_width=True,
    hide_index=True,
)