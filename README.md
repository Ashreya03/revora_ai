# Revora AI

## Revenue Recovery Intelligence

Revora AI is an AI-powered revenue recovery intelligence platform that identifies customers at risk, estimates revenue exposure, recommends recovery actions, executes bounded recovery workflows, and measures recovered revenue.

> Built as an independent prototype for the Razorpay AI Buildathon 2026 – AI Revenue Recovery track.

---

## 🚨 Important Data Note

The customer dataset used in this project is the synthetic **SaaS Subscription & Churn Analytics Dataset (RavenStack)**.

The original dataset does not contain real payment-failure or payment-recovery data.

Therefore, payment events and recovery outcomes in this project are **synthetic demonstration data** generated from the customer risk signals.

No real customer payments or real money are processed by this project.

---

# 1. Problem

Failed payments can create significant revenue leakage for subscription businesses.

A failed payment does not necessarily mean permanent customer loss.

Different failures may require different recovery strategies:

- Temporary network or bank errors → retry
- Expired cards → payment link
- Insufficient funds → retry later
- High-value/high-risk customers → priority outreach
- Repeated failures → human escalation

A simple rule-based retry system may treat every failed payment the same.

Revora AI aims to make recovery more intelligent by combining:

**Customer Risk + Revenue Exposure + Payment Failure + Recovery Decision + Outcome**

---

# 2. Solution

Revora AI follows an end-to-end revenue recovery workflow:

```text
Customer Data
      ↓
Feature Engineering
      ↓
Churn Risk Model
      ↓
Revenue at Risk
      ↓
Decision Engine
      ↓
Failed Payment
      ↓
Recovery Agent
      ↓
Smart Retry / Payment Link / Outreach
      ↓
Recovery Attempts
      ↓
Recovered OR Human Escalation
      ↓
Audit Trail
      ↓
Revenue Analytics + AI Assistant