import streamlit as st

from data_loader import load_customer_risk_data


# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = load_customer_risk_data()


# --------------------------------------------------
# Page Header
# --------------------------------------------------

st.title("Decision Center")

st.caption(
    "Prioritized retention actions based on churn risk and revenue exposure"
)


# --------------------------------------------------
# Priority Summary
# --------------------------------------------------

high_df = df[df["priority"] == "High"]
medium_df = df[df["priority"] == "Medium"]
low_df = df[df["priority"] == "Low"]


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "High Priority",
        f"{len(high_df):,}",
        f"${high_df['revenue_at_risk'].sum():,.0f} at risk"
    )


with col2:
    st.metric(
        "Medium Priority",
        f"{len(medium_df):,}",
        f"${medium_df['revenue_at_risk'].sum():,.0f} at risk"
    )


with col3:
    st.metric(
        "Low Priority",
        f"{len(low_df):,}",
        f"${low_df['revenue_at_risk'].sum():,.0f} at risk"
    )


st.divider()


# --------------------------------------------------
# Priority Sections
# --------------------------------------------------

priority_order = [
    ("High", high_df),
    ("Medium", medium_df),
    ("Low", low_df)
]


for priority, priority_df in priority_order:

    if len(priority_df) == 0:
        continue

    priority_df = priority_df.sort_values(
        "revenue_at_risk",
        ascending=False
    )

    total_revenue = priority_df["revenue_at_risk"].sum()

    st.subheader(
        f"{priority} Priority"
    )

    st.caption(
        f"{len(priority_df):,} customers • "
        f"${total_revenue:,.0f} estimated revenue at risk"
    )


    # Show top 15
    display_df = priority_df.head(15).copy()


    display_columns = [
        "account_id",
        "plan_tier",
        "churn_probability",
        "revenue_at_risk",
        "recommended_action"
    ]


    st.dataframe(
        display_df[display_columns],
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

            "recommended_action": st.column_config.TextColumn(
                "Recommended Action",
                width="large"
            )
        }
    )


    if len(priority_df) > 15:

        st.caption(
            f"Showing top 15 of {len(priority_df):,} "
            f"{priority.lower()} priority customers"
        )


    st.divider()