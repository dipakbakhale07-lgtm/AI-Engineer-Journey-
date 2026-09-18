import json
import streamlit as st

from business_agent import run_agent_request


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Project 4 — Business Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #f7f9fc;
        color: #172033;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #172033 !important;
    }

    p, span, label, div {
        color: #243047;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e4e9f1;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #172033 !important;
    }

    .brand-box {
        padding: 10px 4px 18px 4px;
        border-bottom: 1px solid #e5eaf2;
        margin-bottom: 22px;
    }

    .brand-title {
        font-size: 26px;
        font-weight: 800;
        color: #172033;
        margin-bottom: 3px;
    }

    .brand-subtitle {
        font-size: 14px;
        color: #68758a;
    }


    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #ffffff 0%,
            #eef5ff 100%
        );
        border: 1px solid #dce7f5;
        border-radius: 22px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 8px 25px rgba(24, 39, 75, 0.06);
    }

    .hero-title {
        font-size: 36px;
        font-weight: 800;
        color: #172033;
        margin-bottom: 8px;
    }

    .hero-text {
        font-size: 16px;
        color: #59677d;
        line-height: 1.6;
    }


    /* ---------- STATUS ---------- */

    .success-banner {
        background: #e9f9ef;
        border: 1px solid #bfe9cc;
        border-radius: 16px;
        padding: 17px 20px;
        margin: 15px 0 24px 0;
    }

    .success-title {
        font-size: 17px;
        font-weight: 750;
        color: #137333;
    }

    .success-text {
        color: #356047;
        font-size: 14px;
        margin-top: 3px;
    }


    .error-banner {
        background: #fff1f1;
        border: 1px solid #f0c4c4;
        border-radius: 16px;
        padding: 17px 20px;
        margin: 15px 0 24px 0;
    }

    .error-title {
        font-size: 17px;
        font-weight: 750;
        color: #b42318;
    }

    .error-text {
        color: #7a2e2e;
        font-size: 14px;
        margin-top: 3px;
    }


    /* ---------- SECTION TITLES ---------- */

    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #172033;
        margin-top: 20px;
        margin-bottom: 12px;
    }


    /* ---------- TOOL CARD ---------- */

    .tool-card {
        background: #eef4ff;
        border: 1px solid #d7e4fa;
        border-radius: 16px;
        padding: 20px 22px;
        min-height: 105px;
    }

    .tool-label {
        color: #66748a;
        font-size: 13px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    .tool-name {
        color: #173d8f;
        font-size: 21px;
        font-weight: 800;
    }


    /* ---------- STATUS CARD ---------- */

    .status-card {
        background: #eaf9f0;
        border: 1px solid #c5ead2;
        border-radius: 16px;
        padding: 20px 22px;
        min-height: 105px;
    }

    .status-label {
        color: #567463;
        font-size: 13px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    .status-value {
        color: #137333;
        font-size: 21px;
        font-weight: 800;
    }


    /* ---------- RESULT CARD ---------- */

    .result-card {
        background: #ffffff;
        border: 1px solid #dfe5ee;
        border-radius: 20px;
        padding: 25px;
        margin-top: 18px;
        box-shadow: 0 6px 20px rgba(24, 39, 75, 0.05);
    }

    .result-header {
        font-size: 23px;
        font-weight: 800;
        color: #172033;
        margin-bottom: 18px;
    }


    /* ---------- ANSWER ---------- */

    .answer-box {
        background: #f0f8ff;
        border-left: 5px solid #3984ff;
        border-radius: 12px;
        padding: 18px 20px;
        margin-top: 12px;
    }

    .answer-label {
        color: #52627a;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 7px;
    }

    .answer-text {
        color: #172033;
        font-size: 18px;
        font-weight: 600;
        line-height: 1.55;
    }


    /* ---------- QUESTION ---------- */

    .question-box {
        background: #f8f9fb;
        border: 1px solid #e5e9ef;
        border-radius: 12px;
        padding: 15px 18px;
        margin-bottom: 15px;
    }

    .question-label {
        color: #68758a;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .question-text {
        color: #172033;
        font-size: 16px;
        font-weight: 600;
    }


    /* ---------- FOLLOW-UP DRAFT ---------- */

    .draft-box {
        background: #fffdf5;
        border: 1px solid #eadfb4;
        border-radius: 16px;
        padding: 22px;
        margin-top: 12px;
    }

    .draft-label {
        color: #75651f;
        font-size: 13px;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 12px;
    }

    .draft-text {
        color: #252525;
        font-size: 16px;
        line-height: 1.7;
        white-space: pre-wrap;
    }


    /* ---------- LEAD CARD ---------- */

    .lead-summary {
        background: #f4f7fb;
        border: 1px solid #e0e6ef;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
    }


    /* ---------- SAFETY ---------- */

    .safety-card {
        background: #effaf3;
        border: 1px solid #c9ead4;
        border-radius: 15px;
        padding: 17px;
        margin-top: 15px;
    }

    .safety-title {
        color: #137333;
        font-weight: 750;
        font-size: 15px;
    }

    .safety-text {
        color: #476653;
        font-size: 13px;
        line-height: 1.55;
        margin-top: 5px;
    }


    /* ---------- INPUT ---------- */

    textarea {
        background: #ffffff !important;
        color: #172033 !important;
        border: 1px solid #cfd7e3 !important;
        border-radius: 14px !important;
    }

    textarea::placeholder {
        color: #8a96a8 !important;
    }


    /* ---------- BUTTON ---------- */

    button[kind="primary"] {
        border-radius: 12px !important;
        font-weight: 700 !important;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #7b8799;
        font-size: 13px;
        margin-top: 45px;
        padding-top: 20px;
        border-top: 1px solid #e1e6ee;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-box">
            <div class="brand-title">🤖 Business Agent</div>
            <div class="brand-subtitle">
                FAQ • Leads • Follow-ups
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ⚡ Example Requests")

    examples = [
        "What are your business hours?",
        "Do you provide home delivery?",
        "Show interested leads",
        "Show qualified leads",
        "What payment methods do you accept?",
        "Create a follow-up draft for Priya"
    ]

    selected_example = st.selectbox(
        "Choose an example",
        ["Select an example"] + examples
    )

    st.markdown("---")

    st.markdown("### 🛡️ Safety")

    st.markdown(
        """
        <div class="safety-card">
            <div class="safety-title">
                🟢 Safety controls active
            </div>
            <div class="safety-text">
                Sending, deleting, updating, and other
                irreversible actions are not automatic.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    with st.expander("⚙️ System"):

        st.write("**Model:** llama3:latest")
        st.write("**Runtime:** Local Ollama")
        st.write("**Maximum tool calls:** 3")
        st.write("**Mode:** Controlled tool use")


# ============================================================
# MAIN HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            🤖 Project 4 — Multi-Tool Business Agent
        </div>

        <div class="hero-text">
            Ask a business question and the AI agent will
            understand the request, select the appropriate
            Python tool, execute it, and present the result
            in a human-friendly format.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# REQUEST AREA
# ============================================================

st.markdown(
    '<div class="section-title">💬 Ask Your Business Agent</div>',
    unsafe_allow_html=True
)

default_request = ""

if selected_example != "Select an example":
    default_request = selected_example

request = st.text_area(
    "Business request",
    value=default_request,
    placeholder=(
        "Example: What are your business hours?"
    ),
    height=110,
    label_visibility="collapsed"
)

run_button = st.button(
    "🚀 Run Business Agent",
    type="primary",
    use_container_width=True
)


# ============================================================
# RUN AGENT
# ============================================================

if run_button:

    if not request.strip():

        st.markdown(
            """
            <div class="error-banner">
                <div class="error-title">
                    ⚠️ Request required
                </div>
                <div class="error-text">
                    Please enter a business request.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        with st.spinner("Agent is processing your request..."):

            result = run_agent_request(
                request.strip()
            )

        # ====================================================
        # ERROR
        # ====================================================

        if not result.get("success"):

            st.markdown(
                """
                <div class="error-banner">
                    <div class="error-title">
                        ⚠️ Request could not be completed
                    </div>
                    <div class="error-text">
                        The agent safely stopped the affected operation.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            error_message = result.get(
                "error",
                "Unknown error."
            )

            st.error(error_message)

        # ====================================================
        # SUCCESS
        # ====================================================

        else:

            tool_name = result.get(
                "tool",
                "Unknown"
            )

            tool_result = result.get(
                "result",
                {}
            )

            st.markdown(
                """
                <div class="success-banner">
                    <div class="success-title">
                        ✅ Request completed successfully
                    </div>
                    <div class="success-text">
                        The agent processed your request using
                        the appropriate tool.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # =================================================
            # TOOL + STATUS
            # =================================================

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    f"""
                    <div class="tool-card">
                        <div class="tool-label">
                            🔧 Selected Tool
                        </div>
                        <div class="tool-name">
                            {tool_name}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(
                    """
                    <div class="status-card">
                        <div class="status-label">
                            🟢 Status
                        </div>
                        <div class="status-value">
                            SUCCESS
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # =================================================
            # RESULT
            # =================================================

            st.markdown(
                """
                <div class="section-title">
                    📊 Result
                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # FAQ RESULT
            # =================================================

            if tool_name == "search_faq":

                question = tool_result.get(
                    "question",
                    request.strip()
                )

                answer = tool_result.get(
                    "answer",
                    "No answer available."
                )

                st.markdown(
                    """
                    <div class="result-card">
                        <div class="result-header">
                            💡 FAQ Answer
                        </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="question-box">
                        <div class="question-label">
                            Question
                        </div>
                        <div class="question-text">
                            {question}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="answer-box">
                        <div class="answer-label">
                            Answer
                        </div>
                        <div class="answer-text">
                            {answer}
                        </div>
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # =================================================
            # LEADS RESULT
            # =================================================

            elif tool_name == "get_leads_by_status":

                status = tool_result.get(
                    "status",
                    "unknown"
                )

                leads = tool_result.get(
                    "leads",
                    []
                )

                count = tool_result.get(
                    "count",
                    len(leads)
                )

                st.markdown(
                    """
                    <div class="result-card">
                        <div class="result-header">
                            👥 Lead Results
                        </div>
                    """,
                    unsafe_allow_html=True
                )

                metric1, metric2 = st.columns(2)

                with metric1:
                    st.metric(
                        "Lead Status",
                        status.title()
                    )

                with metric2:
                    st.metric(
                        "Total Leads",
                        count
                    )

                if leads:

                    lead_rows = []

                    for lead in leads:

                        lead_rows.append(
                            {
                                "Name": lead.get(
                                    "name",
                                    "-"
                                ),
                                "Status": lead.get(
                                    "status",
                                    "-"
                                ).title(),
                                "Interest": lead.get(
                                    "interest",
                                    "-"
                                )
                            }
                        )

                    st.table(
                        lead_rows
                    )

                else:

                    st.info(
                        "No leads found for this status."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            # =================================================
            # FOLLOW-UP RESULT
            # =================================================

            elif tool_name == "generate_followup_draft":

                name = tool_result.get(
                    "name",
                    "Lead"
                )

                lead_status = tool_result.get(
                    "lead_status",
                    ""
                )

                interest = tool_result.get(
                    "interest",
                    ""
                )

                draft = tool_result.get(
                    "draft",
                    "No draft generated."
                )

                st.markdown(
                    """
                    <div class="result-card">
                        <div class="result-header">
                            ✉️ Follow-Up Draft
                        </div>
                    """,
                    unsafe_allow_html=True
                )

                info1, info2, info3 = st.columns(3)

                with info1:
                    st.metric(
                        "Lead",
                        name
                    )

                with info2:
                    st.metric(
                        "Status",
                        lead_status.title()
                    )

                with info3:
                    st.metric(
                        "Interest",
                        interest
                    )

                st.markdown(
                    f"""
                    <div class="draft-box">
                        <div class="draft-label">
                            Draft Message
                        </div>
                        <div class="draft-text">
                            {draft}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.caption(
                    "🔒 Draft only — no message was sent."
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            # =================================================
            # FALLBACK
            # =================================================

            else:

                st.markdown(
                    """
                    <div class="result-card">
                        <div class="result-header">
                            📋 Tool Result
                        </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write(tool_result)

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


# ============================================================
# AVAILABLE TOOLS
# ============================================================

st.markdown(
    '<div class="section-title">🧰 Available Tools</div>',
    unsafe_allow_html=True
)

tool_col1, tool_col2, tool_col3 = st.columns(3)

with tool_col1:

    st.info(
        "🔎 **search_faq()**\n\n"
        "Answers supported business FAQ questions."
    )

with tool_col2:

    st.info(
        "👥 **get_leads_by_status()**\n\n"
        "Retrieves leads using their business status."
    )

with tool_col3:

    st.info(
        "✉️ **generate_followup_draft()**\n\n"
        "Creates a follow-up draft without sending it."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Project 4 — Multi-Tool Business Agent
        • Ollama + Llama 3
        • Python Tools
        • Controlled Tool Use
        • Human-Safe Actions
    </div>
    """,
    unsafe_allow_html=True
)