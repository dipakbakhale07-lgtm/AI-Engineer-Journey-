import json


LEADS = [
    {
        "name": "Rahul",
        "status": "new",
        "interest": "AI automation"
    },
    {
        "name": "Priya",
        "status": "interested",
        "interest": "chatbot"
    },
    {
        "name": "Amit",
        "status": "qualified",
        "interest": "RAG system"
    },
    {
        "name": "Sneha",
        "status": "interested",
        "interest": "AI content"
    },
    {
        "name": "Vikram",
        "status": "contacted",
        "interest": "AI agents"
    }
]


def get_leads_by_status(status):
    if not status or not status.strip():
        return {
            "success": False,
            "error": "Lead status is required.",
            "leads": []
        }

    status = status.strip().lower()

    matching_leads = [
        lead for lead in LEADS
        if lead["status"] == status
    ]

    return {
        "success": True,
        "status": status,
        "count": len(matching_leads),
        "leads": matching_leads
    }


if __name__ == "__main__":
    test_statuses = [
        "interested",
        "new",
        "qualified",
        "contacted",
        ""
    ]

    for status in test_statuses:
        result = get_leads_by_status(status)
        print(json.dumps(result, indent=2))
        print("-" * 50)