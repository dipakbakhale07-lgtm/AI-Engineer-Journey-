import json
import requests


INPUT_FILE = "content_inputs.json"
OUTPUT_FILE = "generated_content.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3:latest"

STYLES = [
    "Technical",
    "Beginner-friendly",
    "Short"
]


# Load structured content inputs
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    content_inputs = json.load(file)


def create_prompt(content, style):
    """Create a strict factual LinkedIn drafting prompt."""

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

1. Use only facts from SOURCE NOTES and KEY LESSON.
2. Do not invent personal experiences.
3. Do not invent achievements or results.
4. Do not invent numbers or statistics.
5. Do not claim improved accuracy, efficiency, speed, time savings, or business results unless explicitly stated.
6. Do not describe the author as a freelancer, developer, professional, business owner, expert, or similar role unless explicitly stated.
7. Do not invent clients, users, deployments, production use, or customers.
8. Do not expand an acronym unless its expansion is provided in the source.
9. Do not add technical concepts that are not supported by the source.
10. Do not use phrases such as "significant improvement", "saving time", "increased accuracy", or similar unsupported outcomes.
11. Do not use "we" for results unless the source explicitly says so.
12. Do not use "[FACT-CHECK NEEDED]". Remove unsupported claims instead.
13. Keep the writing simple and natural.
14. The post must describe the same real work regardless of style.

STYLE REQUIREMENTS:

Technical:
Focus on the actual technical workflow and concepts present in the source.

Beginner-friendly:
Explain the same information using simple English.

Short:
Keep only the most important facts.

OUTPUT EXACTLY IN THIS FORMAT:

Hook:
<one or two sentences>

Body:
<5-8 short lines>

Lesson:
<one or two sentences>

CTA:
<use the provided CTA without adding new claims>

Hashtags:
<relevant hashtags>

Do not add an introduction.
Do not write "Here is the LinkedIn post".
Do not add explanations outside the required format.
"""


def generate_with_ollama(prompt):
    """Generate one draft using local Ollama."""

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
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()


def find_unsupported_phrases(text):
    """Detect common hallucinated or unsupported claims."""

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
    """Check that the required Day 19 structure exists."""

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


def generate_safe_draft(content, style, max_attempts=3):
    """Generate and validate a draft."""

    prompt = create_prompt(content, style)

    for attempt in range(1, max_attempts + 1):

        post = generate_with_ollama(prompt)

        bad_phrases = find_unsupported_phrases(post)
        missing_sections = validate_structure(post)

        if not bad_phrases and not missing_sections:
            return post, prompt, True

        print(f"  Validation failed (attempt {attempt})")

        if bad_phrases:
            print(f"  Unsupported phrases: {', '.join(bad_phrases)}")

        if missing_sections:
            print(f"  Missing sections: {', '.join(missing_sections)}")

        prompt += """

IMPORTANT CORRECTION:

Your previous draft failed validation.

Generate the post again.

Remove every unsupported claim.
Do not use any forbidden phrase.
Follow the exact output structure.
Use ONLY the supplied source information.
"""

    return post, prompt, False


# Generate drafts
drafts = []

# Day 19 requires three styles.
# We generate them for the first three structured content inputs.
for content in content_inputs[:3]:

    for style in STYLES:

        print(f"Generating: {content['topic']} - {style}")

        try:
            post, prompt, valid = generate_safe_draft(
                content,
                style
            )

        except Exception as error:
            post = f"[GENERATION ERROR] {error}"
            prompt = create_prompt(content, style)
            valid = False

        drafts.append({
            "topic": content["topic"],
            "style": style,
            "prompt": prompt,
            "generated_post": post,
            "validation_passed": valid
        })


# Save results
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(
        drafts,
        file,
        indent=4,
        ensure_ascii=False
    )


valid_count = sum(
    1 for draft in drafts
    if draft["validation_passed"]
)


print()
print("Day 19 AI drafting workflow completed.")
print(f"Total drafts generated: {len(drafts)}")
print(f"Validation passed: {valid_count}/{len(drafts)}")
print(f"Saved to: {OUTPUT_FILE}")
print()