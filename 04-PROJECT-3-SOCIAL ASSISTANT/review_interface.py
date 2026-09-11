import streamlit as st
import json
import os
import subprocess
import sys
from datetime import datetime


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="SocialAI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

GENERATED_FILE = "generated_content.json"
INPUT_FILE = "content_inputs.json"
REVIEWED_FILE = "reviewed_posts.json"


# ============================================================
# MODERN COLORFUL UI
# ============================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 8% 5%,
            rgba(124, 58, 237, 0.14),
            transparent 28%
        ),
        radial-gradient(
            circle at 92% 8%,
            rgba(14, 165, 233, 0.12),
            transparent 28%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(236, 72, 153, 0.08),
            transparent 35%
        ),
        #f8fafc;

    color: #111827;
}


/* =========================================================
   FORCE MAIN TEXT DARK
   ========================================================= */

html,
body,
[class*="css"] {
    color: #111827;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #f5f3ff 48%,
        #eff6ff 100%
    );

    border-right: 1px solid #dbe3ef;
}

[data-testid="stSidebar"] * {
    color: #111827 !important;
}


/* =========================================================
   HEADINGS
   ========================================================= */

.hero {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1.5px;

    background: linear-gradient(
        90deg,
        #6d28d9,
        #2563eb,
        #db2777
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    font-size: 17px;
    color: #475569 !important;
    margin-bottom: 25px;
}


/* =========================================================
   CARDS
   ========================================================= */

.card {
    background: #ffffff;
    color: #111827 !important;

    border: 1px solid #e2e8f0;
    border-radius: 24px;

    padding: 24px;

    box-shadow:
        0 12px 35px rgba(15, 23, 42, 0.07);

    margin-bottom: 18px;
}

.gradient-card {
    background: linear-gradient(
        135deg,
        #f5f3ff,
        #eef6ff,
        #fff1f8
    );

    color: #111827 !important;

    border: 1px solid #e2e8f0;
    border-radius: 24px;

    padding: 24px;

    box-shadow:
        0 12px 35px rgba(15, 23, 42, 0.06);
}


/* =========================================================
   POST PREVIEW
   ========================================================= */

.post-preview {
    background: #ffffff;
    color: #111827 !important;

    border: 1px solid #dbe3ef;
    border-radius: 20px;

    padding: 24px;

    box-shadow:
        0 8px 25px rgba(15, 23, 42, 0.06);

    white-space: pre-wrap;
    line-height: 1.7;
}


/* =========================================================
   INPUTS
   ========================================================= */

.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stRadio label,
.stCheckbox label {
    color: #1f2937 !important;
    font-weight: 600 !important;
}


/* Text inputs */

.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #111827 !important;

    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
}


/* Placeholder */

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}


/* Select boxes */

.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #111827 !important;

    border-radius: 12px !important;
}

.stSelectbox div[data-baseweb="select"] * {
    color: #111827 !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton button {
    color: #ffffff !important;

    background: linear-gradient(
        90deg,
        #7c3aed,
        #2563eb
    ) !important;

    border: none !important;
    border-radius: 14px !important;

    font-weight: 700 !important;

    min-height: 44px;

    transition: 0.2s;
}

.stButton button:hover {
    opacity: 0.90;
    transform: translateY(-1px);
}


/* Disabled buttons */

.stButton button:disabled {
    background: #cbd5e1 !important;
    color: #64748b !important;
}


/* =========================================================
   METRICS
   ========================================================= */

[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.90);

    border: 1px solid #e2e8f0;
    border-radius: 18px;

    padding: 14px;
}

[data-testid="stMetricLabel"] {
    color: #475569 !important;
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
}


/* =========================================================
   CHECKBOXES
   ========================================================= */

.stCheckbox label {
    color: #1f2937 !important;
}


/* =========================================================
   CAPTIONS
   ========================================================= */

[data-testid="stCaptionContainer"] {
    color: #64748b !important;
}


/* =========================================================
   EXPANDERS
   ========================================================= */

[data-testid="stExpander"] {
    background: #ffffff;

    border: 1px solid #e2e8f0;
    border-radius: 18px;
}

[data-testid="stExpander"] * {
    color: #111827;
}


/* =========================================================
   FEATURE CARDS
   ========================================================= */

.feature {
    background: rgba(255, 255, 255, 0.90);
    color: #111827;

    border-radius: 18px;

    padding: 18px;

    border: 1px solid #e2e8f0;

    text-align: center;
}

.big-number {
    font-size: 28px;
    font-weight: 800;
    color: #111827 !important;
}

.small-text {
    color: #64748b !important;
    font-size: 13px;
}


/* =========================================================
   ALERTS
   ========================================================= */

[data-testid="stAlert"] {
    color: #111827 !important;
}


/* =========================================================
   DIVIDERS
   ========================================================= */

hr {
    border-color: #dbe3ef !important;
}


/* =========================================================
   SCROLLBAR
   ========================================================= */

::-webkit-scrollbar {
    width: 9px;
}

::-webkit-scrollbar-track {
    background: #eef2f7;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(
        180deg,
        #7c3aed,
        #2563eb
    );

    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(
        180deg,
        #6d28d9,
        #1d4ed8
    );
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA FUNCTIONS
# ============================================================

def load_json(filename, default):

    if not os.path.exists(filename):
        return default

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return default


def save_json(filename, data):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def normalize_posts(data):

    result = []

    for item in data:

        topic = item.get(
            "topic",
            "Untitled Topic"
        )

        versions = item.get("versions")

        if isinstance(versions, dict):

            for style, content in versions.items():

                if isinstance(content, dict):

                    text = content.get(
                        "generated_post",
                        ""
                    )

                else:

                    text = str(content)

                result.append({
                    "topic": topic,
                    "style": style,
                    "content": text,
                    "status": item.get(
                        "status",
                        "DRAFT"
                    )
                })

        else:

            result.append({
                "topic": topic,
                "style": item.get(
                    "style",
                    "Unknown"
                ),
                "content": item.get(
                    "generated_post",
                    ""
                ),
                "status": item.get(
                    "status",
                    "DRAFT"
                )
            })

    return result


# ============================================================
# LOAD CONTENT
# ============================================================

generated_data = load_json(
    GENERATED_FILE,
    []
)

posts = normalize_posts(
    generated_data
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:

    st.session_state.page = "Home"


if "posts" not in st.session_state:

    st.session_state.posts = posts


if "reviewed_data" not in st.session_state:

    st.session_state.reviewed_data = load_json(
        REVIEWED_FILE,
        []
    )


posts = st.session_state.posts
reviewed_data = st.session_state.reviewed_data


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## ✨ SocialAI"
    )

    st.caption(
        "Your personal AI content workspace"
    )

    st.divider()

    navigation = st.radio(
        "WORKSPACE",
        [
            "Home",
            "Create",
            "Drafts",
            "Review",
            "Tracker"
        ],
        index=[
            "Home",
            "Create",
            "Drafts",
            "Review",
            "Tracker"
        ].index(
            st.session_state.page
        )
    )

    st.session_state.page = navigation

    st.divider()

    st.markdown(
        "### 📊 Overview"
    )

    total = len(posts)

    drafts = sum(
        1
        for p in posts
        if p.get("status") == "DRAFT"
    )

    reviews = sum(
        1
        for p in posts
        if p.get("status") == "REVIEW"
    )

    approved = sum(
        1
        for p in posts
        if p.get("status") == "APPROVED"
    )

    posted = sum(
        1
        for p in posts
        if p.get("status") == "POSTED"
    )

    st.metric(
        "Total Posts",
        total
    )

    st.metric(
        "In Review",
        reviews
    )

    st.metric(
        "Approved",
        approved
    )

    st.metric(
        "Posted",
        posted
    )

    st.divider()

    st.caption(
        "🔐 Human approval is required before publishing."
    )


# ============================================================
# HOME
# ============================================================

if navigation == "Home":

    st.markdown(
        '<div class="hero">'
        'Your Social Media Assistant ✨'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Create useful content from your real AI-building journey.'
        '</div>',
        unsafe_allow_html=True
    )

    a, b, c, d = st.columns(4)

    with a:

        st.markdown(
            f"""
            <div class="feature">
                <div class="big-number">{total}</div>
                <div class="small-text">Total Posts</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with b:

        st.markdown(
            f"""
            <div class="feature">
                <div class="big-number">{drafts}</div>
                <div class="small-text">Drafts</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c:

        st.markdown(
            f"""
            <div class="feature">
                <div class="big-number">{reviews}</div>
                <div class="small-text">In Review</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with d:

        st.markdown(
            f"""
            <div class="feature">
                <div class="big-number">{approved}</div>
                <div class="small-text">Approved</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    left, right = st.columns(
        [1.35, 1]
    )

    with left:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 🧠 Your AI content workspace"
        )

        st.write(
            "SocialAI helps turn your real project work "
            "into useful social-media content."
        )

        st.markdown("""
        **✍️ Create**

        Start from something you actually built or learned.

        **🧠 Generate**

        Transform your source material into structured content.

        **🎨 Adapt**

        Create different writing styles.

        **🔍 Review**

        Check truth, usefulness, privacy and claims.

        **👤 Approve**

        Keep the human in control.

        **📊 Track**

        Follow every post through its lifecycle.
        """)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    with right:

        st.markdown(
            '<div class="gradient-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 🚀 Ready to create?"
        )

        st.write(
            "Start with your real project experience."
        )

        if st.button(
            "✨ Create New Post",
            use_container_width=True
        ):

            st.session_state.page = "Create"

            st.rerun()

        st.write("")

        st.info(
            "SocialAI does not invent your experience "
            "or automatically publish your content."
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# CREATE
# ============================================================

elif navigation == "Create":

    st.markdown(
        '<div class="hero">'
        'Create Content ✨'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Give the assistant real information and create a useful post.'
        '</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(
        [1.35, 1]
    )

    with left:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 📝 What do you want to share?"
        )

        topic = st.text_input(
            "Topic",
            placeholder=(
                "Example: What I learned while building a RAG Assistant"
            )
        )

        source_notes = st.text_area(
            "Your real experience / source notes",
            height=180,
            placeholder=(
                "Describe what you actually built, learned "
                "or experienced..."
            )
        )

        audience = st.text_input(
            "Audience",
            value=(
                "AI builders, Python learners and potential clients"
            )
        )

        lesson = st.text_area(
            "Key lesson",
            height=100,
            placeholder="What is the main lesson?"
        )

        cta = st.text_input(
            "Call to Action",
            placeholder="Optional"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    with right:

        st.markdown(
            '<div class="gradient-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 🎯 Customize your content"
        )

        platform = st.selectbox(
            "Platform",
            [
                "LinkedIn",
                "Instagram",
                "X"
            ]
        )

        style = st.selectbox(
            "Writing style",
            [
                "Technical",
                "Beginner-friendly",
                "Short"
            ]
        )

        tone = st.selectbox(
            "Tone",
            [
                "Professional",
                "Educational",
                "Friendly",
                "Practical"
            ]
        )

        st.markdown(
            "### 🛡️ Content protection"
        )

        st.checkbox(
            "Use only my real experience",
            value=True
        )

        st.checkbox(
            "Avoid unsupported claims",
            value=True
        )

        st.checkbox(
            "Protect private information",
            value=True
        )

        st.checkbox(
            "Human approval required",
            value=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    st.write("")

    if st.button(
        "✨ Generate Social Media Content",
        use_container_width=True
    ):

        if not topic.strip():

            st.warning(
                "Please enter a topic."
            )

        elif not source_notes.strip():

            st.warning(
                "Please provide your real source notes."
            )

        else:

            new_input = {
                "topic": topic,
                "source_notes": source_notes,
                "audience": audience,
                "key_lesson": lesson,
                "call_to_action": cta
            }

            try:

                existing_inputs = load_json(
                    INPUT_FILE,
                    []
                )

                existing_inputs.append(
                    new_input
                )

                save_json(
                    INPUT_FILE,
                    existing_inputs
                )

                with st.spinner(
                    "✨ Creating your content..."
                ):

                    result = subprocess.run(
                        [
                            sys.executable,
                            "content_generator.py"
                        ],
                        capture_output=True,
                        text=True
                    )

                if result.returncode == 0:

                    st.session_state.posts = normalize_posts(
                        load_json(
                            GENERATED_FILE,
                            []
                        )
                    )

                    st.success(
                        "🎉 Content generated successfully!"
                    )

                    st.info(
                        f"Platform: {platform}  •  "
                        f"Style: {style}  •  "
                        f"Tone: {tone}"
                    )

                    st.session_state.page = "Drafts"

                    st.rerun()

                else:

                    st.error(
                        "The content generator returned an error."
                    )

                    if result.stderr:

                        st.code(
                            result.stderr
                        )

            except Exception as error:

                st.error(
                    f"Generation failed: {error}"
                )


# ============================================================
# DRAFTS
# ============================================================

elif navigation == "Drafts":

    st.markdown(
        '<div class="hero">'
        'Your Drafts 📝'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Browse and edit your generated content.'
        '</div>',
        unsafe_allow_html=True
    )

    if not posts:

        st.info(
            "No drafts yet. Create your first post."
        )

    for index, post in enumerate(posts):

        status = post.get(
            "status",
            "DRAFT"
        )

        with st.expander(
            f"✨ {post['topic']}  •  "
            f"{post['style']}  •  {status}"
        ):

            edited = st.text_area(
                "Post content",
                value=post["content"],
                height=240,
                key=f"draft_editor_{index}"
            )

            if st.button(
                "💾 Save Draft",
                key=f"save_draft_{index}"
            ):

                post["content"] = edited

                save_json(
                    GENERATED_FILE,
                    posts
                )

                st.success(
                    "Draft saved successfully."
                )


# ============================================================
# REVIEW
# ============================================================

elif navigation == "Review":

    st.markdown(
        '<div class="hero">'
        'Human Review 🔍'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'The final quality gate — you make the decision.'
        '</div>',
        unsafe_allow_html=True
    )

    if not posts:

        st.info(
            "No content available for review."
        )

    else:

        selected = st.selectbox(
            "Choose a post",
            range(len(posts)),
            format_func=lambda i:
                f"{posts[i]['topic']} — "
                f"{posts[i]['style']}"
        )

        post = posts[selected]

        st.markdown(
            '<div class="post-preview">',
            unsafe_allow_html=True
        )

        st.markdown(
            f"### {post['topic']}"
        )

        st.caption(
            f"Style: {post['style']}"
        )

        st.markdown(
            f"**Current status:** `{post.get('status', 'DRAFT')}`"
        )

        st.markdown(
            post["content"]
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        st.write("")

        edited_content = st.text_area(
            "Edit your post before approval",
            value=post["content"],
            height=220,
            key=f"review_editor_{selected}"
        )

        st.markdown(
            "### 🛡️ Quality Checklist"
        )

        col1, col2 = st.columns(2)

        with col1:

            true_check = st.checkbox(
                "✓ Is it true?",
                key=f"true_check_{selected}"
            )

            useful_check = st.checkbox(
                "✓ Is it useful?",
                key=f"useful_check_{selected}"
            )

            private_check = st.checkbox(
                "✓ No private data",
                key=f"private_check_{selected}"
            )

        with col2:

            secret_check = st.checkbox(
                "✓ No secret / API key",
                key=f"secret_check_{selected}"
            )

            exaggeration_check = st.checkbox(
                "✓ No exaggerated claim",
                key=f"exaggeration_check_{selected}"
            )

        st.divider()

        current_status = post.get(
            "status",
            "DRAFT"
        )

        st.markdown(
            f"### Workflow: "
            f"`DRAFT → REVIEW → APPROVED → POSTED`"
        )

        st.markdown(
            f"Current status: **{current_status}**"
        )

        b1, b2, b3 = st.columns(3)

        with b1:

            if st.button(
                "🔄 Move to REVIEW",
                use_container_width=True
            ):

                post["content"] = edited_content

                post["status"] = "REVIEW"

                save_json(
                    GENERATED_FILE,
                    posts
                )

                st.success(
                    "Post moved to REVIEW."
                )

                st.rerun()

        with b2:

            if st.button(
                "❌ Reject",
                use_container_width=True
            ):

                post["content"] = edited_content

                post["status"] = "DRAFT"

                save_json(
                    GENERATED_FILE,
                    posts
                )

                st.warning(
                    "Post returned to DRAFT."
                )

                st.rerun()

        with b3:

            all_checks_pass = (
                true_check
                and useful_check
                and private_check
                and secret_check
                and exaggeration_check
            )

            approve_allowed = (
                current_status == "REVIEW"
                and all_checks_pass
            )

            if st.button(
                "✅ Approve",
                disabled=not approve_allowed,
                use_container_width=True
            ):

                post["content"] = edited_content

                post["status"] = "APPROVED"

                review_record = {

                    "topic": post["topic"],

                    "style": post["style"],

                    "content": edited_content,

                    "status": "APPROVED",

                    "human_approved": True,

                    "reviewed_at": datetime.now().isoformat(),

                    "checks": {

                        "is_true": True,

                        "is_useful": True,

                        "no_private_data": True,

                        "no_secret_api_key": True,

                        "no_exaggerated_claim": True
                    }
                }

                reviewed_data.append(
                    review_record
                )

                save_json(
                    REVIEWED_FILE,
                    reviewed_data
                )

                save_json(
                    GENERATED_FILE,
                    posts
                )

                st.success(
                    "🎉 Human approval recorded successfully!"
                )

                st.rerun()


# ============================================================
# TRACKER
# ============================================================

elif navigation == "Tracker":

    st.markdown(
        '<div class="hero">'
        'Content Tracker 📊'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Track every post through the complete workflow.'
        '</div>',
        unsafe_allow_html=True
    )

    if not posts:

        st.info(
            "No content to track."
        )

    for index, post in enumerate(posts):

        status = post.get(
            "status",
            "DRAFT"
        )

        progress = {

            "DRAFT": 0.25,

            "REVIEW": 0.50,

            "APPROVED": 0.75,

            "POSTED": 1.0

        }.get(
            status,
            0.25
        )

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(
            [4, 1.3, 0.6]
        )

        with c1:

            st.markdown(
                f"### {post['topic']}"
            )

            st.caption(
                f"Style: {post['style']}"
            )

        with c2:

            st.markdown(
                f"**{status}**"
            )

        with c3:

            st.write(
                f"#{index + 1}"
            )

        st.progress(
            progress
        )

        st.caption(
            "DRAFT  →  REVIEW  →  APPROVED  →  POSTED"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "✨ SocialAI Assistant • "
    "Create intelligently • "
    "Review responsibly • "
    "Publish manually"
)