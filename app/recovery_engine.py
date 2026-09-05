import pandas as pd
import hashlib


# ============================================================
# FILE PATHS
# ============================================================

PAYMENT_FILE = "data/synthetic/payment_events.csv"

OUTPUT_FILE = "data/processed/recovery_decisions.csv"

AUDIT_FILE = "data/processed/recovery_audit_log.csv"


# ============================================================
# LOAD DATA
# ============================================================

payments = pd.read_csv(PAYMENT_FILE)


# ============================================================
# CHOOSE RECOVERY ACTION
# ============================================================

def choose_action(row, attempt):

    risk = row["churn_probability"]
    amount = row["amount"]
    failure = row["failure_reason"]

    # -------------------------
    # ATTEMPT 1
    # -------------------------

    if attempt == 1:

        if risk >= 0.50 and amount >= 7500:
            return "Priority customer outreach"

        if failure in ["network_error", "bank_error"]:
            return "Smart retry"

        if failure in ["expired_card", "card_declined"]:
            return "Payment link"

        if failure == "insufficient_funds":
            return "Retry later"

        return "Payment link"

    # -------------------------
    # ATTEMPT 2
    # -------------------------

    if attempt == 2:

        if failure == "insufficient_funds":
            return "Payment link"

        if failure in ["network_error", "bank_error"]:
            return "Payment link"

        return "Customer outreach"

    # -------------------------
    # ATTEMPT 3
    # -------------------------

    if attempt == 3:
        return "Final recovery attempt"

    return "Stop"


# ============================================================
# SIMULATE RECOVERY RESULT
# ============================================================

def simulate_attempt(
    payment_id,
    action,
    risk,
    attempt
):

    probabilities = {

        "Smart retry": 0.65,

        "Retry later": 0.55,

        "Payment link": 0.70,

        "Priority customer outreach": 0.80,

        "Customer outreach": 0.65,

        "Final recovery attempt": 0.45,
    }

    probability = probabilities.get(
        action,
        0.40
    )

    # Higher risk = slightly harder recovery
    probability -= risk * 0.10

    # Later attempts are harder
    probability -= (attempt - 1) * 0.08

    # Deterministic result
    key = (
        f"{payment_id}-"
        f"{attempt}-"
        f"{action}"
    )

    hash_value = int(
        hashlib.md5(
            key.encode()
        ).hexdigest()[:8],
        16
    )

    score = (
        hash_value % 10000
    ) / 10000

    if score < probability:
        return "recovered"

    return "failed"


# ============================================================
# PROCESS PAYMENTS
# ============================================================

final_records = []

audit_records = []


for _, payment in payments.iterrows():

    # ========================================================
    # SUCCESSFUL PAYMENT
    # ========================================================

    if payment["payment_status"] == "successful":

        final_records.append(
            {
                "payment_id": payment["payment_id"],

                "account_id": payment["account_id"],

                "amount": payment["amount"],

                "payment_status": "successful",

                "failure_reason": "",

                "attempts_used": 0,

                "recovery_action": "No action",

                "recovery_status": "not_required",

                # IMPORTANT:
                # Successful payments are NOT recovered revenue.
                "recovered_amount": 0,

                "next_step": "No action",
            }
        )

        continue


    # ========================================================
    # FAILED PAYMENT
    # ========================================================

    recovered = False

    attempts_used = 0

    final_action = ""

    final_status = "failed"


    # Maximum 3 recovery attempts
    for attempt in range(1, 4):

        action = choose_action(
            payment,
            attempt
        )

        result = simulate_attempt(
            payment["payment_id"],
            action,
            payment["churn_probability"],
            attempt
        )

        attempts_used = attempt


        # ====================================================
        # AUDIT LOG
        # ====================================================

        audit_records.append(
            {
                "payment_id":
                    payment["payment_id"],

                "account_id":
                    payment["account_id"],

                "attempt_number":
                    attempt,

                "action":
                    action,

                "result":
                    result,

                "amount":
                    payment["amount"],

                "churn_probability":
                    payment["churn_probability"],

                "failure_reason":
                    payment["failure_reason"],
            }
        )


        # ====================================================
        # RECOVERED
        # ====================================================

        if result == "recovered":

            recovered = True

            final_action = action

            final_status = "recovered"

            break


    # ========================================================
    # FINAL RESULT
    # ========================================================

    if recovered:

        recovered_amount = payment["amount"]

        next_step = "Recovered - stop"

    else:

        recovered_amount = 0

        next_step = "Escalate to human"

        final_action = "Recovery exhausted"


    final_records.append(
        {
            "payment_id":
                payment["payment_id"],

            "account_id":
                payment["account_id"],

            "amount":
                payment["amount"],

            "payment_status":
                "failed",

            "failure_reason":
                payment["failure_reason"],

            "attempts_used":
                attempts_used,

            "recovery_action":
                final_action,

            "recovery_status":
                final_status,

            "recovered_amount":
                recovered_amount,

            "next_step":
                next_step,
        }
    )


# ============================================================
# CREATE DATAFRAMES
# ============================================================

recovery_decisions = pd.DataFrame(
    final_records
)

audit_log = pd.DataFrame(
    audit_records
)


# ============================================================
# SAVE FILES
# ============================================================

recovery_decisions.to_csv(
    OUTPUT_FILE,
    index=False
)

audit_log.to_csv(
    AUDIT_FILE,
    index=False
)


# ============================================================
# CALCULATE METRICS
# ============================================================

failed_payments = recovery_decisions[
    recovery_decisions["payment_status"] == "failed"
]

recovered_payments = recovery_decisions[
    (recovery_decisions["payment_status"] == "failed")
    &
    (recovery_decisions["recovery_status"] == "recovered")
]

escalated_payments = recovery_decisions[
    recovery_decisions["next_step"]
    == "Escalate to human"
]


# ============================================================
# RECOVERY RATE
# ============================================================

if len(failed_payments) > 0:

    recovery_rate = (
        len(recovered_payments)
        /
        len(failed_payments)
    )

else:

    recovery_rate = 0


# ============================================================
# RECOVERED REVENUE
# ============================================================

revenue_recovered = (
    recovered_payments["recovered_amount"]
    .sum()
)


# ============================================================
# STILL AT RISK
# ============================================================

failed_payment_value = (
    failed_payments["amount"].sum()
)

still_at_risk = (
    failed_payment_value
    -
    revenue_recovered
)


# ============================================================
# OUTPUT
# ============================================================

print("=" * 60)

print(
    "REVORA AI - MULTI-STEP RECOVERY ENGINE"
)

print("=" * 60)

print()

print(
    "Total payment events:",
    len(recovery_decisions)
)

print(
    "Failed payments:",
    len(failed_payments)
)

print(
    "Recovered payments:",
    len(recovered_payments)
)

print(
    "Recovery rate:",
    f"{recovery_rate:.1%}"
)

print(
    "Revenue recovered:",
    f"${revenue_recovered:,.2f}"
)

print(
    "Still at risk:",
    f"${still_at_risk:,.2f}"
)

print(
    "Human escalations:",
    len(escalated_payments)
)

print()

print(
    "Average attempts per failed payment:",
    f"{failed_payments['attempts_used'].mean():.2f}"
)

print()

print(
    "Audit events:",
    len(audit_log)
)

print()

print("Recovery outcomes:")

print(
    failed_payments[
        "recovery_status"
    ].value_counts()
)

print()

print("Recovery actions:")

print(
    audit_log[
        "action"
    ].value_counts()
)

print()

print("Saved recovery decisions to:")

print(OUTPUT_FILE)

print()

print("Saved audit log to:")

print(AUDIT_FILE)

print("=" * 60)