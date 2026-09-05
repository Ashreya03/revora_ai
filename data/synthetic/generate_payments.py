import pandas as pd
import numpy as np


# ============================================================
# SETTINGS
# ============================================================

np.random.seed(42)

CUSTOMER_FILE = "../processed/customer_risk_decisions.csv"
OUTPUT_FILE = "payment_events.csv"


# ============================================================
# LOAD CUSTOMER RISK DATA
# ============================================================

customers = pd.read_csv(CUSTOMER_FILE)

print("Customers loaded:", len(customers))


# ============================================================
# GENERATE PAYMENT EVENTS
# ============================================================

events = []

for _, customer in customers.iterrows():

    account_id = customer["account_id"]
    mrr = customer["current_mrr"]
    churn_probability = customer["churn_probability"]

    # Higher-risk customers are more likely
    # to experience a failed payment in our
    # synthetic demonstration data.

    failure_probability = min(
        0.10 + churn_probability * 0.55,
        0.75
    )

    payment_failed = np.random.random() < failure_probability

    if payment_failed:

        failure_reason = np.random.choice(
            [
                "insufficient_funds",
                "card_declined",
                "expired_card",
                "bank_error",
                "network_error"
            ],
            p=[
                0.30,
                0.25,
                0.15,
                0.15,
                0.15
            ]
        )

        payment_status = "failed"

    else:

        failure_reason = ""

        payment_status = "successful"


    events.append(
        {
            "payment_id": f"P-{len(events) + 1:05d}",
            "account_id": account_id,
            "amount": round(mrr, 2),
            "payment_status": payment_status,
            "failure_reason": failure_reason,
            "attempt_number": 1,
            "churn_probability": round(
                churn_probability,
                4
            )
        }
    )


# ============================================================
# CREATE DATAFRAME
# ============================================================

payments = pd.DataFrame(events)


# ============================================================
# SAVE DATA
# ============================================================

payments.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# RESULTS
# ============================================================

print()
print("Payment events generated:", len(payments))

print()
print("Payment status:")
print(
    payments["payment_status"].value_counts()
)

print()
print("Sample:")
print(
    payments.head(10)
)

print()
print("Saved to:")
print(OUTPUT_FILE)