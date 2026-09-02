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
# LOAD LEADS
# -------------------------------

def load_leads():

    with open(DATA_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


# -------------------------------
# MAIN PROGRAM
# -------------------------------

def main():

    print("\n🤖 AI LEAD CLASSIFICATION AGENT")
    print("=" * 45)

    prompt = load_prompt()
    leads = load_leads()

    print(f"\nLoaded {len(leads)} leads.\n")

    results = []

    # Test first 10 leads
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

            print(f"Error processing Lead {index}: {error}\n")

    # -------------------------------
    # SAVE TEST RESULTS
    # -------------------------------

    with open(RESULTS_FILE, "w", encoding="utf-8") as file:

        file.write("# Day 12 — Lead Classification Test Results\n\n")

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
    print("✅ Testing completed!")
    print(f"📄 Results saved to: {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()
