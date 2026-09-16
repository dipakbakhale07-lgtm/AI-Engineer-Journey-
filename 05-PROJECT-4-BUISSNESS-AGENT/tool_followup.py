import json


def generate_followup_draft(name, lead_status, interest):
    if not name or not name.strip():
        return {
            "success": False,
            "error": "Lead name is required.",
            "draft": None
        }

    if not lead_status or not lead_status.strip():
        return {
            "success": False,
            "error": "Lead status is required.",
            "draft": None
        }

    if not interest or not interest.strip():
        return {
            "success": False,
            "error": "Lead interest is required.",
            "draft": None
        }

    name = name.strip()
    lead_status = lead_status.strip().lower()
    interest = interest.strip()

    draft = (
        f"Hi {name},\n\n"
        f"Thanks for your interest in {interest}. "
        f"I wanted to follow up regarding your enquiry. "
        f"Please let me know if you would like more information "
        f"or would like to discuss the next steps.\n\n"
        f"Best regards"
    )

    return {
        "success": True,
        "name": name,
        "lead_status": lead_status,
        "interest": interest,
        "draft": draft
    }


if __name__ == "__main__":
    test_cases = [
        {
            "name": "Priya",
            "lead_status": "interested",
            "interest": "chatbot"
        },
        {
            "name": "Amit",
            "lead_status": "qualified",
            "interest": "RAG system"
        },
        {
            "name": "",
            "lead_status": "interested",
            "interest": "chatbot"
        }
    ]

    for case in test_cases:
        result = generate_followup_draft(
            case["name"],
            case["lead_status"],
            case["interest"]
        )
        print(json.dumps(result, indent=2))
        print("-" * 50)