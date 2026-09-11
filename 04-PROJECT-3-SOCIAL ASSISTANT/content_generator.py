import json
import requests


# ============================================================
# CONFIG
# ============================================================

INPUT_FILE = "content_inputs.json"
OUTPUT_FILE = "generated_content.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:latest"

# Day 20 needs 3 posts ready for human review.
# We use one style for each of the first 3 real content inputs.
POST_CONFIG = [
    ("Technical", 0),
    ("Beginner-friendly", 1),
    ("Short", 2)
]


# ============================================================
# LOAD CONTENT INPUTS
# ============================================================

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as file:

    content_inputs = json.load(file)


# ============================================================
# PROMPT
# ============================================================

def create_prompt(content, style):

    return f"""
You are a factual LinkedIn content drafting assistant.

Create ONE LinkedIn post using ONLY the information supplied below.

TOPIC:
{content["topic"]}

SOURCE NOTES:
{content["source_notes"]}

AUDIENCE:
{content["audience"]}

KEY LESSON:
{content["key_lesson"]}

CALL TO ACTION:
{content["call_to_action"]}

STYLE:
{style}

STRICT RULES:

1. Use ONLY facts from SOURCE NOTES and KEY LESSON.
2. Do not invent personal experiences.
3. Do not invent achievements or results.
4. Do not invent numbers or statistics.
5. Do not claim improved accuracy, efficiency, speed,
   time savings, or business results unless explicitly stated.
6. Do not describe the author as a freelancer, developer,
   professional, expert, business owner, or similar role
   unless explicitly stated.
7. Do not invent clients, customers, users, deployments,
   production use, revenue, or business outcomes.
8. Do not expand acronyms unless the source provides the expansion.
9. Do not add technical concepts not supported by the source.
10. Do not exaggerate the work.
11. Do not use unsupported claims.
12. Do not use "[FACT-CHECK NEEDED]".
13. Use simple, natural English.
14. Keep the same facts regardless of style.
15. Do not mention information outside the supplied source.
16. Do not say "we" unless the source explicitly says so.

STYLE RULES:

Technical:
Focus on the actual technical workflow and concepts.

Beginner-friendly:
Explain the same information using simple English.

Short:
Keep only the most important information.

OUTPUT EXACTLY:

Hook:
<one or two sentences>

Body:
<5-8 short lines>

Lesson:
<one or two sentences>

CTA:
<use the supplied CTA>

Hashtags:
<relevant hashtags>

Do not add an introduction.
Do not explain your answer.
Do not add text outside this structure.
"""


# ============================================================
# OLLAMA GENERATION
# ============================================================

def generate_with_ollama(prompt):

    response = requests.post(

        OLLAMA_URL,

        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,

            "options": {
                "temperature": 0.2
            }
        },

        timeout=90
    )

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()


# ============================================================
# VALIDATION
# ============================================================

def find_unsupported_phrases(text):

    text_lower = text.lower()

    forbidden_phrases = [

        "recurrent attention-based generator",

        "retrieve, answer, generate",

        "as a freelancer",

        "as a developer",

        "as a professional",

        "as a business owner",

        "saving time",

        "save time",

        "saves time",

        "significant improvement",

        "significant improvements",

        "increased accuracy",

        "improved accuracy",

        "improving accuracy",

        "more efficiently",

        "more effective",

        "increased efficiency",

        "improved efficiency",

        "we saw",

        "our results",

        "customers",

        "clients",

        "production",

        "users",

        "revenue",

        "conversion rate"
    ]

    found = []

    for phrase in forbidden_phrases:

        if phrase in text_lower:

            found.append(phrase)

    return found


def validate_structure(text):

    required_sections = [

        "Hook:",
        "Body:",
        "Lesson:",
        "CTA:",
        "Hashtags:"
    ]

    missing = []

    for section in required_sections:

        if section.lower() not in text.lower():

            missing.append(section)

    return missing


# ============================================================
# GENERATE ONE SAFE DRAFT
# ============================================================

def generate_safe_draft(
    content,
    style
):

    prompt = create_prompt(
        content,
        style
    )

    try:

        post = generate_with_ollama(
            prompt
        )

        bad_phrases = find_unsupported_phrases(
            post
        )

        missing_sections = validate_structure(
            post
        )

        valid = (
            not bad_phrases
            and not missing_sections
        )

        return (
            post,
            prompt,
            valid,
            bad_phrases,
            missing_sections
        )

    except Exception as error:

        return (
            f"[GENERATION ERROR] {error}",
            prompt,
            False,
            [],
            []
        )


# ============================================================
# GENERATE 3 POSTS
# ============================================================

drafts = []

print()
print("Starting Day 20 content generation...")
print("Generating 3 posts for human review.")
print()


for style, input_index in POST_CONFIG:

    if input_index >= len(content_inputs):

        print(
            f"Skipping {style}: "
            f"content input {input_index + 1} does not exist."
        )

        continue

    content = content_inputs[input_index]

    print(
        f"Generating: "
        f"{content['topic']} - {style}"
    )

    (
        post,
        prompt,
        valid,
        bad_phrases,
        missing_sections
    ) = generate_safe_draft(
        content,
        style
    )

    if bad_phrases:

        print(
            "  Unsupported phrases detected: "
            + ", ".join(bad_phrases)
        )

    if missing_sections:

        print(
            "  Missing sections: "
            + ", ".join(missing_sections)
        )

    print(
        f"  Validation: "
        f"{'PASSED' if valid else 'FAILED'}"
    )

    drafts.append({

        "topic": content["topic"],

        "style": style,

        "prompt": prompt,

        "generated_post": post,

        "validation_passed": valid,

        "status": "DRAFT",

        "human_approved": False
    })


# ============================================================
# SAVE OUTPUT
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        drafts,
        file,
        indent=4,
        ensure_ascii=False
    )


# ============================================================
# SUMMARY
# ============================================================

valid_count = sum(

    1
    for draft in drafts

    if draft["validation_passed"]
)


print()
print("=" * 55)
print("DAY 20 CONTENT GENERATION COMPLETED")
print("=" * 55)
print(
    f"Total drafts generated: {len(drafts)}"
)
print(
    f"Validation passed: "
    f"{valid_count}/{len(drafts)}"
)
print(
    f"Saved to: {OUTPUT_FILE}"
)
print("=" * 55)
print()