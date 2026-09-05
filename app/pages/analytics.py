import streamlit as st
import pandas as pd

from data_loader import load_customer_risk_data
from components.cards import kpi_card


# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = load_customer_risk_data()


# --------------------------------------------------
# Page Header
# --------------------------------------------------

st.title("Analytics")

st.caption(
    "Detailed analysis of customer risk, revenue exposure, and subscription segments"
)


# --------------------------------------------------
# KPI ROW
# --------------------------------------------------

total_revenue = df["revenue_at_risk"].sum()

avg_risk = df["churn_probability"].mean()

high_risk_revenue = df.loc[
    df["priority"] == "High",
    "revenue_at_risk"
].sum()

high_risk_percentage = (
    (df["priority"] == "High").mean()
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        "Revenue at Risk",
        f"${total_revenue:,.0f}"
    )

with col2:
    kpi_card(
        "Average Churn Risk",
        f"{avg_risk:.1%}"
    )

with col3:
    kpi_card(
        "High-Risk Revenue",
        f"${high_risk_revenue:,.0f}"
    )

with col4:
    kpi_card(
        "High-Risk Customers",
        f"{high_risk_percentage:.1%}"
    )


st.divider()


# --------------------------------------------------
# RISK ANALYSIS
# --------------------------------------------------

st.subheader("Risk Analysis")

chart_col1, chart_col2 = st.columns(2)


# Churn distribution
with chart_col1:

    st.write("Churn Probability Distribution")

    churn_bins = pd.cut(
        df["churn_probability"],
        bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
        labels=[
            "0–20%",
            "20–40%",
            "40–60%",
            "60–80%",
            "80–100%"
        ],
        include_lowest=True
    )

    churn_distribution = (
        churn_bins
        .value_counts()
        .sort_index()
    )

    st.bar_chart(churn_distribution)


# Revenue by plan
with chart_col2:

    st.write("Revenue at Risk by Plan")

    revenue_by_plan = (
        df.groupby("plan_tier")["revenue_at_risk"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(revenue_by_plan)


st.divider()


# --------------------------------------------------
# PLAN ANALYSIS
# --------------------------------------------------

st.subheader("Plan-Level Risk Analysis")

plan_analysis = (
    df.groupby("plan_tier")
    .agg(
        customers=("account_id", "count"),
        average_churn=("churn_probability", "mean"),
        revenue_at_risk=("revenue_at_risk", "sum")
    )
    .reset_index()
    .sort_values(
        "revenue_at_risk",
        ascending=False
    )
)

st.dataframe(
    plan_analysis,
    hide_index=True,
    use_container_width=True,
    column_config={
        "plan_tier": st.column_config.TextColumn(
            "Plan"
        ),

        "customers": st.column_config.NumberColumn(
            "Customers",
            format="%d"
        ),

        "average_churn": st.column_config.ProgressColumn(
            "Avg Churn Risk",
            format="%.1f%%",
            min_value=0,
            max_value=1
        ),

        "revenue_at_risk": st.column_config.NumberColumn(
            "Revenue at Risk",
            format="$%d"
        )
    }
)


st.divider()


# --------------------------------------------------
# RISK VS REVENUE
# --------------------------------------------------

st.subheader("Customer Risk vs Revenue Exposure")

st.caption(
    "Customers with both high churn probability and high revenue exposure "
    "should generally receive the strongest attention."
)

scatter_data = df[
    [
        "churn_probability",
        "revenue_at_risk"
    ]
].copy()

scatter_data["churn_probability"] = (
    scatter_data["churn_probability"] * 100
)

st.scatter_chart(
    scatter_data,
    x="churn_probability",
    y="revenue_at_risk"
)


st.divider()


# --------------------------------------------------
# TOP REVENUE EXPOSURE
# --------------------------------------------------

st.subheader("Highest Revenue Exposure")

top_customers = (
    df.sort_values(
        "revenue_at_risk",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_customers[
        [
            "account_id",
            "plan_tier",
            "churn_probability",
            "revenue_at_risk",
            "priority",
            "recommended_action"
        ]
    ],
    hide_index=True,
    use_container_width=True,
    column_config={

        "account_id": st.column_config.TextColumn(
            "Account"
        ),

        "plan_tier": st.column_config.TextColumn(
            "Plan"
        ),

        "churn_probability": st.column_config.ProgressColumn(
            "Churn Risk",
            format="%.1f%%",
            min_value=0,
            max_value=1
        ),

        "revenue_at_risk": st.column_config.NumberColumn(
            "Revenue at Risk",
            format="$%d"
        ),

        "priority": st.column_config.TextColumn(
            "Priority"
        ),

        "recommended_action": st.column_config.TextColumn(
            "Recommended Action",
            width="large"
        )
    }
)