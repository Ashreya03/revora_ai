import streamlit as st
import pandas as pd

from components.cards import kpi_card


# ============================================================
# LOAD DATA
# ============================================================

RECOVERY_FILE = "data/processed/recovery_decisions.csv"
AUDIT_FILE = "data/processed/recovery_audit_log.csv"

recovery = pd.read_csv(RECOVERY_FILE)
audit = pd.read_csv(AUDIT_FILE)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("Recovery Center")

st.caption(
    "AI-powered recovery monitoring, decisioning, and audit intelligence."
)

st.info(
    "🧪 **Synthetic Demo Data** — Payment events and recovery outcomes "
    "shown here are simulated for demonstration purposes."
)


# ============================================================
# FILTERS
# ============================================================

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    status_options = [
        "All",
        "Recovered",
        "Failed",
        "Not Required"
    ]

    selected_status = st.selectbox(
        "Recovery Status",
        status_options
    )

with filter_col2:

    action_options = (
        ["All"]
        + sorted(
            recovery["recovery_action"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    selected_action = st.selectbox(
        "Recovery Action",
        action_options
    )


filtered = recovery.copy()


if selected_status != "All":

    if selected_status == "Recovered":

        filtered = filtered[
            filtered["recovery_status"] == "recovered"
        ]

    elif selected_status == "Failed":

        filtered = filtered[
            (filtered["payment_status"] == "failed")
            &
            (filtered["recovery_status"] == "failed")
        ]

    else:

        filtered = filtered[
            filtered["recovery_status"] == "not_required"
        ]


if selected_action != "All":

    filtered = filtered[
        filtered["recovery_action"] == selected_action
    ]


# ============================================================
# CORE METRICS
# ============================================================

failed = recovery[
    recovery["payment_status"] == "failed"
]

recovered = recovery[
    (recovery["payment_status"] == "failed")
    &
    (recovery["recovery_status"] == "recovered")
]

escalated = recovery[
    recovery["next_step"] == "Escalate to human"
]

failed_value = failed["amount"].sum()

revenue_recovered = recovered[
    "recovered_amount"
].sum()

still_at_risk = (
    failed_value - revenue_recovered
)

recovery_rate = (
    len(recovered) / len(failed)
    if len(failed) > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    kpi_card(
        "Failed Payments",
        f"{len(failed):,}",
        "Payments requiring recovery"
    )

with col2:

    kpi_card(
        "Recovery Rate",
        f"{recovery_rate:.1%}",
        f"{len(recovered)} of {len(failed)} recovered"
    )

with col3:

    kpi_card(
        "Revenue Recovered",
        f"${revenue_recovered:,.0f}",
        "From previously failed payments"
    )

with col4:

    kpi_card(
        "Human Escalations",
        f"{len(escalated):,}",
        "Recovery attempts exhausted"
    )


# ============================================================
# REVENUE SUMMARY
# ============================================================

st.divider()

st.subheader("Revenue Recovery Impact")

impact_col1, impact_col2 = st.columns(2)

with impact_col1:

    kpi_card(
        "Failed Payment Value",
        f"${failed_value:,.0f}",
        "Synthetic failed-payment exposure"
    )

with impact_col2:

    kpi_card(
        "Still at Risk",
        f"${still_at_risk:,.0f}",
        "Unrecovered failed-payment value"
    )


# ============================================================
# RECOVERY PERFORMANCE
# ============================================================

st.divider()

st.subheader("Recovery Performance")

chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    st.write("Recovery Outcomes")

    outcome_data = pd.Series(
        {
            "Recovered": len(recovered),
            "Still Failed": len(failed) - len(recovered),
            "Human Escalated": len(escalated),
        }
    )

    st.bar_chart(
        outcome_data
    )


with chart_col2:

    st.write("Recovery Actions")

    action_data = (
        audit["action"]
        .value_counts()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        action_data
    )


# ============================================================
# STRATEGY PERFORMANCE
# ============================================================

st.divider()

st.subheader("Recovery Strategy Performance")

strategy_data = failed.copy()

strategy_performance = (
    strategy_data
    .groupby("recovery_action")
    .agg(
        payments=(
            "payment_id",
            "count"
        ),
        recovered=(
            "recovery_status",
            lambda x:
                (x == "recovered").sum()
        ),
        revenue_recovered=(
            "recovered_amount",
            "sum"
        ),
        payment_value=(
            "amount",
            "sum"
        ),
        avg_attempts=(
            "attempts_used",
            "mean"
        )
    )
    .reset_index()
)

strategy_performance["recovery_rate"] = (
    strategy_performance["recovered"]
    /
    strategy_performance["payments"]
)

strategy_performance["revenue_recovery_rate"] = (
    strategy_performance["revenue_recovered"]
    /
    strategy_performance["payment_value"]
)

strategy_performance = strategy_performance.sort_values(
    "revenue_recovered",
    ascending=False
)


st.dataframe(
    strategy_performance,
    hide_index=True,
    use_container_width=True,
    column_config={

        "recovery_action":
            st.column_config.TextColumn(
                "Strategy"
            ),

        "payments":
            st.column_config.NumberColumn(
                "Cases",
                format="%d"
            ),

        "recovered":
            st.column_config.NumberColumn(
                "Recovered",
                format="%d"
            ),

        "recovery_rate":
            st.column_config.ProgressColumn(
                "Recovery Rate",
                format="%.1f%%",
                min_value=0,
                max_value=1
            ),

        "revenue_recovered":
            st.column_config.NumberColumn(
                "Revenue Recovered",
                format="$%d"
            ),

        "payment_value":
            st.column_config.NumberColumn(
                "Payment Value",
                format="$%d"
            ),

        "revenue_recovery_rate":
            st.column_config.ProgressColumn(
                "Value Recovery",
                format="%.1f%%",
                min_value=0,
                max_value=1
            ),

        "avg_attempts":
            st.column_config.NumberColumn(
                "Avg Attempts",
                format="%.2f"
            )
    }
)


# ============================================================
# RECOVERY DECISIONS
# ============================================================

st.divider()

st.subheader("Recovery Decisions")

st.caption(
    f"Showing {len(filtered):,} of {len(recovery):,} payment events."
)

display_columns = [
    "payment_id",
    "account_id",
    "amount",
    "failure_reason",
    "attempts_used",
    "recovery_action",
    "recovery_status",
    "recovered_amount",
    "next_step"
]

st.dataframe(
    filtered[
        display_columns
    ].sort_values(
        "amount",
        ascending=False
    ),
    hide_index=True,
    use_container_width=True,
    column_config={

        "payment_id":
            st.column_config.TextColumn(
                "Payment"
            ),

        "account_id":
            st.column_config.TextColumn(
                "Account"
            ),

        "amount":
            st.column_config.NumberColumn(
                "Amount",
                format="$%d"
            ),

        "failure_reason":
            st.column_config.TextColumn(
                "Failure Reason"
            ),

        "attempts_used":
            st.column_config.NumberColumn(
                "Attempts",
                format="%d"
            ),

        "recovery_action":
            st.column_config.TextColumn(
                "Final Action"
            ),

        "recovery_status":
            st.column_config.TextColumn(
                "Status"
            ),

        "recovered_amount":
            st.column_config.NumberColumn(
                "Recovered",
                format="$%d"
            ),

        "next_step":
            st.column_config.TextColumn(
                "Next Step"
            )
    }
)


# ============================================================
# HUMAN ESCALATIONS
# ============================================================

st.divider()

st.subheader("Human Escalations")

if len(escalated) == 0:

    st.success(
        "No payments currently require human intervention."
    )

else:

    st.warning(
        f"{len(escalated)} payment cases exhausted "
        "the automated recovery workflow."
    )

    st.dataframe(
        escalated[
            [
                "payment_id",
                "account_id",
                "amount",
                "failure_reason",
                "attempts_used",
                "recovery_action",
                "next_step"
            ]
        ].sort_values(
            "amount",
            ascending=False
        ),
        hide_index=True,
        use_container_width=True,
        column_config={

            "payment_id":
                st.column_config.TextColumn(
                    "Payment"
                ),

            "account_id":
                st.column_config.TextColumn(
                    "Account"
                ),

            "amount":
                st.column_config.NumberColumn(
                    "Amount",
                    format="$%d"
                ),

            "attempts_used":
                st.column_config.NumberColumn(
                    "Attempts"
                ),

            "recovery_action":
                st.column_config.TextColumn(
                    "Last Action"
                ),

            "next_step":
                st.column_config.TextColumn(
                    "Next Step"
                )
        }
    )


# ============================================================
# AUDIT TRAIL
# ============================================================

st.divider()

st.subheader("Recovery Audit Trail")

st.caption(
    "Every automated recovery attempt is recorded for traceability."
)

st.dataframe(
    audit.sort_values(
        [
            "payment_id",
            "attempt_number"
        ]
    ),
    hide_index=True,
    use_container_width=True,
    column_config={

        "payment_id":
            st.column_config.TextColumn(
                "Payment"
            ),

        "account_id":
            st.column_config.TextColumn(
                "Account"
            ),

        "attempt_number":
            st.column_config.NumberColumn(
                "Attempt"
            ),

        "action":
            st.column_config.TextColumn(
                "Action"
            ),

        "result":
            st.column_config.TextColumn(
                "Result"
            ),

        "amount":
            st.column_config.NumberColumn(
                "Amount",
                format="$%d"
            ),

        "churn_probability":
            st.column_config.ProgressColumn(
                "Risk",
                format="%.1f%%",
                min_value=0,
                max_value=1
            ),

        "failure_reason":
            st.column_config.TextColumn(
                "Failure Reason"
            )
    }
)