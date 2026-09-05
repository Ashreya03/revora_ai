import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# CONFIG
# ============================================================

load_dotenv(override=True)

client = OpenAI()

MODEL = "gpt-5.6-luna"

CUSTOMER_FILE = "data/processed/customer_risk_decisions.csv"
RECOVERY_FILE = "data/processed/recovery_decisions.csv"
AUDIT_FILE = "data/processed/recovery_audit_log.csv"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_customer_data():
    return pd.read_csv(CUSTOMER_FILE)


@st.cache_data
def load_recovery_data():
    return pd.read_csv(RECOVERY_FILE)


@st.cache_data
def load_audit_data():
    return pd.read_csv(AUDIT_FILE)


# ============================================================
# RECOVERY METRICS
# ============================================================

def get_recovery_metrics():

    recovery = load_recovery_data()

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

    recovered_value = recovered[
        "recovered_amount"
    ].sum()

    still_at_risk = (
        failed_value - recovered_value
    )

    recovery_rate = (
        len(recovered) / len(failed)
        if len(failed) > 0
        else 0
    )

    return {
        "total_payment_events": len(recovery),
        "failed_payments": len(failed),
        "recovered_payments": len(recovered),
        "recovery_rate": recovery_rate,
        "revenue_recovered": recovered_value,
        "still_at_risk": still_at_risk,
        "human_escalations": len(escalated),
    }


# ============================================================
# STRATEGY PERFORMANCE
# ============================================================

def get_strategy_performance():

    recovery = load_recovery_data()

    failed = recovery[
        recovery["payment_status"] == "failed"
    ].copy()

    if failed.empty:
        return pd.DataFrame()

    strategy = (
        failed
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

            total_payment_value=(
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

    strategy["recovery_rate"] = (
        strategy["recovered"]
        /
        strategy["payments"]
    )

    strategy["revenue_recovery_rate"] = (
        strategy["revenue_recovered"]
        /
        strategy["total_payment_value"]
    )

    strategy = strategy.sort_values(
        "revenue_recovered",
        ascending=False
    )

    return strategy


# ============================================================
# CUSTOMER CONTEXT
# ============================================================

def get_customer_context(account_id):

    customers = load_customer_data()

    recovery = load_recovery_data()

    customer = customers[
        customers["account_id"] == account_id
    ]

    payment = recovery[
        recovery["account_id"] == account_id
    ]

    if customer.empty:
        return None

    customer = customer.iloc[0]

    context = {
        "account_id": account_id,
        "plan_tier": customer["plan_tier"],
        "current_mrr": customer["current_mrr"],
        "churn_probability": customer["churn_probability"],
        "revenue_at_risk": customer["revenue_at_risk"],
        "priority": customer["priority"],
        "recommended_action": customer["recommended_action"],
        "avg_satisfaction": customer["avg_satisfaction"],
        "ticket_count": customer["ticket_count"],
        "escalation_rate": customer["escalation_rate"],
        "total_usage_count": customer["total_usage_count"],
    }

    if not payment.empty:

        payment = payment.iloc[0]

        context.update({
            "payment_id": payment["payment_id"],
            "payment_amount": payment["amount"],
            "payment_status": payment["payment_status"],
            "failure_reason": payment["failure_reason"],
            "attempts_used": payment["attempts_used"],
            "recovery_action": payment["recovery_action"],
            "recovery_status": payment["recovery_status"],
            "recovered_amount": payment["recovered_amount"],
            "next_step": payment["next_step"],
        })

    return context


# ============================================================
# CUSTOMER AI
# ============================================================

def build_ai_prompt(account_id, question):

    context = get_customer_context(account_id)

    if context is None:
        return None

    return f"""
You are Revora AI, an AI revenue recovery analyst.

Analyze this customer using ONLY the supplied data.

Customer context:
{context}

User question:
{question}

Rules:

1. Do not invent facts.
2. Separate observed data, model predictions,
   and recommendations.
3. Explain decisions clearly.
4. If recovery information exists,
   explain the recovery action and outcome.
5. Payment data is synthetic demonstration data.

Give a concise business-focused answer.
"""


def ask_ai_assistant(account_id, question):

    prompt = build_ai_prompt(
        account_id,
        question
    )

    if prompt is None:
        return "Customer not found."

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are Revora AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ============================================================
# RECOVERY AI
# ============================================================

def build_recovery_prompt(question):

    metrics = get_recovery_metrics()

    strategy = get_strategy_performance()

    audit = load_audit_data()

    strategy_records = []

    for _, row in strategy.iterrows():

        strategy_records.append({
            "strategy":
                row["recovery_action"],

            "payments":
                int(row["payments"]),

            "recovered":
                int(row["recovered"]),

            "recovery_rate":
                f"{row['recovery_rate']:.1%}",

            "revenue_recovered":
                f"${row['revenue_recovered']:,.2f}",

            "revenue_recovery_rate":
                f"{row['revenue_recovery_rate']:.1%}",

            "average_attempts":
                round(row["avg_attempts"], 2)
        })

    return f"""
You are Revora AI's Recovery Intelligence Agent.

User question:
{question}

==================================================
OVERALL RECOVERY RESULTS
==================================================

Total payment events:
{metrics["total_payment_events"]}

Failed payments:
{metrics["failed_payments"]}

Recovered payments:
{metrics["recovered_payments"]}

Recovery rate:
{metrics["recovery_rate"]:.1%}

Revenue recovered:
${metrics["revenue_recovered"]:,.2f}

Still at risk:
${metrics["still_at_risk"]:,.2f}

Human escalations:
{metrics["human_escalations"]}

Audit events:
{len(audit)}

==================================================
STRATEGY PERFORMANCE
==================================================

{strategy_records}

==================================================
HOW TO INTERPRET STRATEGIES
==================================================

Use:

- Recovery rate to measure effectiveness.
- Revenue recovered to measure financial impact.
- Revenue recovery rate to compare recovered value
  against the value assigned to each strategy.
- Number of payments to understand sample size.
- Average attempts to understand operational effort.

If asked "which strategy performed best":

Do NOT simply choose the strategy with the highest
recovery rate if it handled very few payments.

Consider both:
1. Recovery rate
2. Revenue recovered
3. Number of payments handled

State the evidence behind the conclusion.

==================================================
IMPORTANT RULES
==================================================

1. These are synthetic demonstration payment events.
2. Never claim these are real transactions.
3. Recovered revenue includes ONLY previously
   failed payments that were successfully recovered.
4. Do not count initially successful payments.
5. Maximum recovery attempts are 3.
6. Recovered payments stop the workflow.
7. Failed payments after maximum attempts
   are escalated to humans.
8. Never invent missing information.
9. Clearly distinguish observed results
   from recommendations.

Answer concisely and use the actual numbers above.
"""


def ask_recovery_ai(question):

    prompt = build_recovery_prompt(question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Revora AI, "
                    "a bounded revenue recovery intelligence agent."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ============================================================
# BUSINESS AI
# ============================================================

def build_business_prompt(question):

    customers = load_customer_data()

    metrics = get_recovery_metrics()

    strategy = get_strategy_performance()

    top_customers = (
        customers
        .sort_values(
            "revenue_at_risk",
            ascending=False
        )
        .head(10)
    )

    return f"""
You are Revora AI, a revenue recovery intelligence agent.

Business question:
{question}

Recovery metrics:

Total payment events:
{metrics["total_payment_events"]}

Failed payments:
{metrics["failed_payments"]}

Recovered payments:
{metrics["recovered_payments"]}

Recovery rate:
{metrics["recovery_rate"]:.1%}

Revenue recovered:
${metrics["revenue_recovered"]:,.2f}

Still at risk:
${metrics["still_at_risk"]:,.2f}

Human escalations:
{metrics["human_escalations"]}

Strategy performance:
{strategy.to_dict(orient="records")}

Top customers by revenue at risk:

{top_customers[
    [
        "account_id",
        "plan_tier",
        "churn_probability",
        "revenue_at_risk",
        "priority",
        "recommended_action"
    ]
].to_dict(orient="records")}

Rules:

- Use only supplied data.
- Do not invent facts.
- Recovered revenue means revenue recovered
  from previously failed payments.
- Payment data is synthetic.
- Separate observations from recommendations.
- Focus on revenue and operational impact.

Give a concise business-focused answer.
"""


def ask_business_ai(question):

    prompt = build_business_prompt(question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are Revora AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content