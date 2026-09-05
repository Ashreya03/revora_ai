import re
import streamlit as st

from ai_engine import (
    ask_ai_assistant,
    ask_business_ai,
    ask_recovery_ai,
)


# ============================================================
# PAGE
# ============================================================

st.title("AI Assistant")

st.caption(
    "Revora Intelligence — customer risk, revenue recovery, "
    "payment decisions, and business insights."
)

st.divider()


# ============================================================
# INTRO
# ============================================================

st.info(
    "🤖 **Revora Intelligence**\n\n"
    "I can analyze customers, failed payments, recovery decisions, "
    "recovered revenue, and business-level risk."
)


# ============================================================
# QUICK QUESTIONS
# ============================================================

st.subheader("Quick Questions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(
        "💰 Recovery Performance",
        use_container_width=True
    ):
        st.session_state.quick_prompt = (
            "How much revenue did we recover and what is our recovery rate?"
        )

with col2:
    if st.button(
        "🔄 Best Recovery Strategy",
        use_container_width=True
    ):
        st.session_state.quick_prompt = (
            "Which recovery strategy performed best?"
        )

with col3:
    if st.button(
        "⚠️ Escalations",
        use_container_width=True
    ):
        st.session_state.quick_prompt = (
            "How many payments were escalated to humans and why?"
        )


st.divider()


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):
        st.write(message["content"])


# ============================================================
# INPUT
# ============================================================

prompt = st.chat_input(
    "Ask Revora AI about customers, payments, or recovery..."
)


# Quick question handling
if "quick_prompt" in st.session_state:

    if not prompt:
        prompt = st.session_state.quick_prompt

    del st.session_state.quick_prompt


# ============================================================
# PROCESS QUESTION
# ============================================================

if prompt:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)


    # --------------------------------------------------------
    # DETECT CUSTOMER
    # --------------------------------------------------------

    account_match = re.search(
        r"A-[a-zA-Z0-9]+",
        prompt
    )


    # --------------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Revora AI is analyzing..."):

            try:

                # Customer-specific question
                if account_match:

                    account_id = (
                        account_match.group(0)
                    )

                    response = ask_ai_assistant(
                        account_id,
                        prompt
                    )

                # Recovery/payment question
                elif any(
                    word in prompt.lower()
                    for word in [
                        "payment",
                        "payments",
                        "recovery",
                        "recover",
                        "recovered",
                        "retry",
                        "failed",
                        "failure",
                        "escalat",
                        "strategy",
                        "attempt"
                    ]
                ):

                    response = ask_recovery_ai(
                        prompt
                    )

                # General business question
                else:

                    response = ask_business_ai(
                        prompt
                    )


            except Exception as e:

                response = (
                    "I couldn't process this request. "
                    "Please check the AI service configuration."
                )

                st.error(
                    f"AI error: {e}"
                )


        st.write(response)


    # --------------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# ============================================================
# CLEAR CHAT
# ============================================================

st.divider()

if st.button(
    "Clear Conversation"
):

    st.session_state.messages = []

    st.rerun()