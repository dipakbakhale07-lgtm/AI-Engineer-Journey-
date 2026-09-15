import json


FAQ_DATA = {
    "business hours": "Our business hours are 9:00 AM to 7:00 PM.",
    "home delivery": "Yes, we provide home delivery within the service area.",
    "payment methods": "We accept cash, UPI, and card payments.",
    "return policy": "Products can be returned according to the business return policy."
}


def search_faq(question):
    if not question or not question.strip():
        return {
            "success": False,
            "error": "Question is required.",
            "answer": None
        }

    question = question.strip().lower()

    for keyword, answer in FAQ_DATA.items():
        if keyword in question:
            return {
                "success": True,
                "question": question,
                "answer": answer
            }

    return {
        "success": False,
        "question": question,
        "error": "No matching FAQ found.",
        "answer": None
    }


if __name__ == "__main__":
    test_questions = [
        "What are your business hours?",
        "Do you provide home delivery?",
        "What payment methods do you accept?",
        "What is your return policy?",
        ""
    ]

    for question in test_questions:
        result = search_faq(question)
        print(json.dumps(result, indent=2))
        print("-" * 50)