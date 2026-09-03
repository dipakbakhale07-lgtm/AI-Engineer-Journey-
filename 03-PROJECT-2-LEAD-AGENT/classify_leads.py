import csv
import json
from pathlib import Path

import ollama


# -------------------------------
# PROJECT PATHS
# -------------------------------

BASE_DIR = Path(__file__).parent

DATA_FILE = BASE_DIR / "dummy_leads.csv"
PROMPT_FILE = BASE_DIR / "classification_prompt.md"
RESULTS_FILE = BASE_DIR / "test-results.md"


# -------------------------------
# LOAD CLASSIFICATION PROMPT
# -------------------------------

def load_prompt():
    return PROMPT_FILE.read_text(encoding="utf-8")


# -------------------------------
# VALIDATE LEAD
# -------------------------------

def validate_lead(lead):
    required_fields = [
        "name",
        "course_interest",
        "lead_message",
        "city",
        "timeline"
    ]

    missing_fields = [
        field for field in required_fields
        if not lead.get(field, "").strip()
    ]

    return missing_fields


# -------------------------------
# CLASSIFY ONE LEAD
# -------------------------------

def classify_lead(lead, prompt):

    lead_information = f"""
Name: {lead.get("name", "")}
Course Interest: {lead.get("course_interest", "")}
Lead Message: {lead.get("lead_message", "")}
City: {lead.get("city", "")}
Timeline: {lead.get("timeline", "")}
"""

    full_prompt = f"""
{prompt}

Now classify the following lead.

LEAD DATA:
{lead_information}

Return only valid JSON.
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


# -------------------------------
# LOAD LEADS FROM CSV
# -------------------------------

def load_leads():

    with open(DATA_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


# -------------------------------
# PROCESS NEW LEAD
# -------------------------------

def process_new_lead(prompt):

    print("\nEnter new lead details:")
    print("-" * 35)

    lead = {
        "name": input("Name: ").strip(),
        "course_interest": input("Course Interest: ").strip(),
        "lead_message": input("Message: ").strip(),
        "city": input("City: ").strip(),
        "timeline": input("Timeline: ").strip()
    }

    missing_fields = validate_lead(lead)

    if missing_fields:
        print("\n❌ Lead validation failed.")

        for field in missing_fields:
            print(f"- Missing: {field}")

        return

    print("\n✅ Lead validation passed.")
    print("🤖 Sending lead to Ollama...")

    try:
        result = classify_lead(lead, prompt)

        print("\n" + "=" * 45)
        print("AI CLASSIFICATION RESULT")
        print("=" * 45)

        print("Category:", result.get("category"))
        print("Priority:", result.get("priority"))
        print("Reason:", result.get("reason"))
        print(
            "Recommended Next Action:",
            result.get("recommended_next_action")
        )
        print("Draft Reply:", result.get("draft_reply"))

        print("\n📦 STRUCTURED JSON")
        print("-" * 45)

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )

        print("\n✅ Lead processed successfully.")

    except Exception as error:
        print(f"\n❌ Error processing lead: {error}")


# -------------------------------
# TEST EXISTING CSV LEADS
# -------------------------------

def test_csv_leads(prompt):

    leads = load_leads()

    print(f"\nLoaded {len(leads)} leads.")
    print("Testing first 10 leads...\n")

    results = []

    for index, lead in enumerate(leads[:10], start=1):

        print(f"Processing Lead {index}...")

        try:
            result = classify_lead(lead, prompt)

            results.append({
                "lead": lead,
                "result": result
            })

            print("Category:", result.get("category"))
            print("Priority:", result.get("priority"))
            print()

        except Exception as error:
            print(f"❌ Error: {error}\n")

    with open(RESULTS_FILE, "w", encoding="utf-8") as file:

        file.write("# Day 13 — Lead Classification Test Results\n\n")

        for index, item in enumerate(results, start=1):

            lead = item["lead"]
            result = item["result"]

            file.write(f"## Lead {index}\n\n")

            file.write("### Input\n\n")

            for key, value in lead.items():
                file.write(f"- **{key}:** {value}\n")

            file.write("\n### AI Classification\n\n")

            file.write(
                f"- **Category:** {result.get('category', '')}\n"
            )

            file.write(
                f"- **Priority:** {result.get('priority', '')}\n"
            )

            file.write(
                f"- **Reason:** {result.get('reason', '')}\n"
            )

            file.write(
                f"- **Recommended Next Action:** "
                f"{result.get('recommended_next_action', '')}\n"
            )

            file.write(
                f"- **Draft Reply:** "
                f"{result.get('draft_reply', '')}\n"
            )

            file.write("\n---\n\n")

    print("=" * 45)
    print("✅ CSV testing completed!")
    print(f"📄 Results saved to: {RESULTS_FILE.name}")


# -------------------------------
# MAIN PROGRAM
# -------------------------------

def main():

    print("\n🤖 AI LEAD CLASSIFICATION AGENT")
    print("=" * 45)

    prompt = load_prompt()

    print("\nChoose an option:")
    print("1. Process a new lead")
    print("2. Test existing CSV leads")

    choice = input("\nEnter choice (1/2): ").strip()

    if choice == "1":
        process_new_lead(prompt)

    elif choice == "2":
        test_csv_leads(prompt)

    else:
        print("\n❌ Invalid choice.")


# -------------------------------
# START PROGRAM
# -------------------------------

if __name__ == "__main__":
    main()