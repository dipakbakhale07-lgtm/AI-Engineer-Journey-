import json
from pathlib import Path

import ollama


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

PROMPT_FILE = BASE_DIR / "classification_prompt.md"
RESULTS_FILE = BASE_DIR / "reply-test-results.md"


# ============================================================
# REPLY TEMPLATES
# ============================================================

REPLY_TEMPLATES = {
    "hot": """
Thank you for your interest. Based on your enquiry, it looks like
you are interested in getting started soon. We can provide the
available course information and help you understand the next steps.
""",

    "warm": """
Thank you for reaching out. We understand that you are exploring
your options. We can share the relevant course information and help
you decide what may be suitable for your goals.
""",

    "cold": """
Thank you for your enquiry. We appreciate your interest. If you
would like more information, we can provide the available course
details and help answer your questions.
"""
}


# ============================================================
# LOAD CLASSIFICATION PROMPT
# ============================================================

def load_prompt():
    return PROMPT_FILE.read_text(encoding="utf-8")


# ============================================================
# GENERATE PERSONALIZED REPLY
# ============================================================

def generate_reply(lead, classification, prompt):

    category = str(
        classification.get("priority", "warm")
    ).lower()

    template = REPLY_TEMPLATES.get(
        category,
        REPLY_TEMPLATES["warm"]
    )

    lead_information = f"""
Name: {lead.get("name", "")}
Course Interest: {lead.get("course_interest", "")}
Lead Message: {lead.get("lead_message", "")}
City: {lead.get("city", "")}
Timeline: {lead.get("timeline", "")}

AI Category: {classification.get("category", "")}
AI Priority: {classification.get("priority", "")}
AI Reason: {classification.get("reason", "")}
"""

    safety_rules = """
IMPORTANT SAFETY AND ACCURACY RULES:

1. Generate a helpful personalized draft reply.
2. Use only information supplied in the lead data or template.
3. Do NOT promise job placement.
4. Do NOT promise a salary.
5. Do NOT promise discounts.
6. Do NOT promise certificates.
7. Do NOT promise internships.
8. Do NOT provide guarantees.
9. Do NOT invent fees, policies, course duration, certificates,
   placement statistics, discounts, schedules, or other business facts.
10. If information is not provided, clearly say that the relevant
    information needs to be confirmed.
11. The reply is ONLY a draft.
12. Do NOT send the message automatically.
13. Keep the reply professional, friendly, and concise.
"""

    full_prompt = f"""
You are an AI lead-reply assistant.

Create a personalized reply for the lead below.

BASE TEMPLATE:
{template}

LEAD INFORMATION:
{lead_information}

{prompt}

{safety_rules}

Return ONLY valid JSON in this format:

{{
    "draft_reply": "your personalized reply",
    "safety_check": "PASS"
}}
"""

    response = ollama.chat(
        model="llama3:latest",
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        format="json"
    )

    result_text = response["message"]["content"]

    return json.loads(result_text)


# ============================================================
# HUMAN APPROVAL
# ============================================================

def ask_for_approval():

    print("\n" + "=" * 55)
    print("HUMAN APPROVAL REQUIRED")
    print("=" * 55)

    print("\nThe reply has NOT been sent.")
    print("Review the draft carefully.")

    approval = input(
        "\nHUMAN_APPROVED (Yes/No): "
    ).strip().lower()

    if approval == "yes":
        return "Yes"

    return "No"


# ============================================================
# PROCESS ONE LEAD
# ============================================================

def process_lead(lead, classification, prompt):

    print("\n🤖 Generating personalized reply...")

    reply_result = generate_reply(
        lead,
        classification,
        prompt
    )

    draft_reply = reply_result.get(
        "draft_reply",
        ""
    )

    safety_check = reply_result.get(
        "safety_check",
        "FAIL"
    )

    print("\n" + "=" * 55)
    print("GENERATED DRAFT REPLY")
    print("=" * 55)

    print(draft_reply)

    print("\nSafety Check:", safety_check)

    if safety_check != "PASS":

        print("\n❌ Safety check failed.")
        print("The reply cannot be approved.")

        return {
            "draft_reply": draft_reply,
            "safety_check": safety_check,
            "HUMAN_APPROVED": "No"
        }

    approval = ask_for_approval()

    if approval == "Yes":

        print("\n✅ HUMAN_APPROVED = Yes")
        print("Reply is approved for manual sending.")

    else:

        print("\n❌ HUMAN_APPROVED = No")
        print("Reply will NOT be sent.")

    return {
        "draft_reply": draft_reply,
        "safety_check": safety_check,
        "HUMAN_APPROVED": approval
    }


# ============================================================
# GET NEXT TEST NUMBER
# ============================================================

def get_next_test_number():

    if not RESULTS_FILE.exists():
        return 1

    content = RESULTS_FILE.read_text(
        encoding="utf-8"
    )

    test_count = content.count("## Test ")

    return test_count + 1


# ============================================================
# SAVE TEST RESULT
# ============================================================

def save_result(
    test_number,
    lead,
    classification,
    reply_result
):

    with open(
        RESULTS_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"\n## Test {test_number}\n\n"
        )

        file.write("### Lead Input\n\n")

        for key, value in lead.items():

            file.write(
                f"- **{key}:** {value}\n"
            )

        file.write("\n### AI Classification\n\n")

        file.write(
            f"- **Category:** "
            f"{classification.get('category', '')}\n"
        )

        file.write(
            f"- **Priority:** "
            f"{classification.get('priority', '')}\n"
        )

        file.write(
            f"- **Reason:** "
            f"{classification.get('reason', '')}\n"
        )

        file.write(
            f"- **Recommended Next Action:** "
            f"{classification.get('recommended_next_action', '')}\n"
        )

        file.write("\n### Draft Reply\n\n")

        file.write(
            reply_result.get(
                "draft_reply",
                ""
            )
        )

        file.write("\n\n### Safety Check\n\n")

        file.write(
            f"{reply_result.get('safety_check', '')}\n"
        )

        file.write("\n### Human Approval\n\n")

        file.write(
            f"**HUMAN_APPROVED:** "
            f"{reply_result.get('HUMAN_APPROVED', 'No')}\n"
        )

        file.write("\n---\n")


# ============================================================
# NEW LEAD INPUT
# ============================================================

def get_new_lead():

    print("\n" + "=" * 55)
    print("ENTER LEAD INFORMATION")
    print("=" * 55)

    return {
        "name": input("Name: ").strip(),
        "course_interest": input(
            "Course Interest: "
        ).strip(),
        "lead_message": input(
            "Message: "
        ).strip(),
        "city": input(
            "City: "
        ).strip(),
        "timeline": input(
            "Timeline: "
        ).strip()
    }


# ============================================================
# CLASSIFY LEAD
# ============================================================

def classify_lead(lead, prompt):

    classification_prompt = f"""
{prompt}

Classify the following lead:

Name: {lead['name']}
Course Interest: {lead['course_interest']}
Lead Message: {lead['lead_message']}
City: {lead['city']}
Timeline: {lead['timeline']}

Return JSON with:

category
priority
reason
recommended_next_action
draft_reply
"""

    response = ollama.chat(
        model="llama3:latest",
        messages=[
            {
                "role": "user",
                "content": classification_prompt
            }
        ],
        format="json"
    )

    return json.loads(
        response["message"]["content"]
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n🤖 AI LEAD REPLY AGENT")
    print("=" * 55)

    prompt = load_prompt()

    lead = get_new_lead()

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    required_fields = [
        "name",
        "course_interest",
        "lead_message",
        "city",
        "timeline"
    ]

    missing_fields = [
        field
        for field in required_fields
        if not lead.get(field)
    ]

    if missing_fields:

        print("\n❌ Missing required information:")

        for field in missing_fields:
            print("-", field)

        return

    print("\n✅ Lead information validated.")

    # --------------------------------------------------------
    # CLASSIFICATION
    # --------------------------------------------------------

    print("\n🤖 Classifying lead...")

    try:

        classification = classify_lead(
            lead,
            prompt
        )

    except Exception as error:

        print(
            f"\n❌ Classification error: {error}"
        )

        return

    print("\n" + "=" * 55)
    print("LEAD CLASSIFICATION")
    print("=" * 55)

    print(
        "Category:",
        classification.get("category")
    )

    print(
        "Priority:",
        classification.get("priority")
    )

    print(
        "Reason:",
        classification.get("reason")
    )

    # --------------------------------------------------------
    # REPLY + HUMAN APPROVAL
    # --------------------------------------------------------

    reply_result = process_lead(
        lead,
        classification,
        prompt
    )

    # --------------------------------------------------------
    # SAVE RESULT WITHOUT OVERWRITING
    # --------------------------------------------------------

    test_number = get_next_test_number()

    if not RESULTS_FILE.exists():

        RESULTS_FILE.write_text(
            "# Day 14 — Reply Agent Test Results\n\n",
            encoding="utf-8"
        )

    save_result(
        test_number,
        lead,
        classification,
        reply_result
    )

    print("\n" + "=" * 55)
    print("✅ DAY 14 TEST COMPLETED")
    print("=" * 55)

    print(
        f"\n📄 Test {test_number} saved to: "
        f"{RESULTS_FILE.name}"
    )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()