import streamlit as st

from data_loader import load_customer_risk_data


# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = load_customer_risk_data()


# --------------------------------------------------
# Page Header
# --------------------------------------------------

st.title("Customers")

st.caption(
    "Explore customer risk, revenue exposure, and recommended interventions"
)


# --------------------------------------------------
# KPI ROW
# --------------------------------------------------

total_customers = len(df)

high_risk = (df["priority"] == "High").sum()

total_revenue_at_risk = df["revenue_at_risk"].sum()


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "High Priority",
        f"{high_risk:,}"
    )

with col3:
    st.metric(
        "Revenue at Risk",
        f"${total_revenue_at_risk:,.0f}"
    )


st.divider()


# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.subheader("Customer Explorer")

filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])


with filter_col1:

    search_id = st.text_input(
        "Search Account",
        placeholder="e.g. A-2d1036"
    )


with filter_col2:

    plan_options = [
        "All"
    ] + sorted(
        df["plan_tier"].dropna().unique().tolist()
    )

    selected_plan = st.selectbox(
        "Plan Tier",
        plan_options
    )


with filter_col3:

    priority_options = [
        "All"
    ] + ["High", "Medium", "Low"]

    selected_priority = st.selectbox(
        "Priority",
        priority_options
    )


# --------------------------------------------------
# Apply Filters
# --------------------------------------------------

filtered_df = df.copy()


if search_id:

    filtered_df = filtered_df[
        filtered_df["account_id"]
        .astype(str)
        .str.contains(
            search_id,
            case=False,
            na=False
        )
    ]


if selected_plan != "All":

    filtered_df = filtered_df[
        filtered_df["plan_tier"] == selected_plan
    ]


if selected_priority != "All":

    filtered_df = filtered_df[
        filtered_df["priority"] == selected_priority
    ]


# --------------------------------------------------
# Results Information
# --------------------------------------------------

st.caption(
    f"Showing {len(filtered_df):,} of {len(df):,} customers"
)


# --------------------------------------------------
# Customer Risk Table
# --------------------------------------------------

display_columns = [
    "account_id",
    "plan_tier",
    "current_mrr",
    "churn_probability",
    "revenue_at_risk",
    "priority",
    "recommended_action"
]


table_data = (
    filtered_df[display_columns]
    .sort_values(
        "revenue_at_risk",
        ascending=False
    )
)


st.dataframe(
    table_data,
    hide_index=True,
    use_container_width=True,
    column_config={

        "account_id": st.column_config.TextColumn(
            "Account"
        ),

        "plan_tier": st.column_config.TextColumn(
            "Plan"
        ),

        "current_mrr": st.column_config.NumberColumn(
            "Current MRR",
            format="$%d"
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