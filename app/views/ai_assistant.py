import re
import streamlit as st

from ai_engine import (
    ask_ai_assistant,
    ask_business_ai
)


# ============================================================
# PAGE
# ============================================================

st.title("AI Assistant")

st.caption(
    "Ask about customer risk, revenue exposure, "
    "priorities, and recommended retention actions."
)

st.divider()


# ============================================================
# INTRO
# ============================================================

st.info(
    "🤖 **Revora Intelligence**\n\n"
    "I can analyze individual customers or answer "
    "business-level revenue recovery questions."
)


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Ask something like: Why is A-58b9ff high risk?"
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if prompt:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)


    # --------------------------------------------------------
    # Detect Account ID
    # --------------------------------------------------------

    account_match = re.search(
        r"A-[a-zA-Z0-9]+",
        prompt
    )


    # --------------------------------------------------------
    # Generate AI response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Analyzing..."):

            try:

                # CUSTOMER QUESTION
                if account_match:

                    account_id = account_match.group(0)

                    response = ask_ai_assistant(
                        account_id,
                        prompt
                    )

                # BUSINESS QUESTION
                else:

                    response = ask_business_ai(
                        prompt
                    )


            except Exception as e:

                response = (
                    "I couldn't process the request. "
                    "Please check the AI service configuration."
                )

                st.error(str(e))


        st.write(response)


    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )