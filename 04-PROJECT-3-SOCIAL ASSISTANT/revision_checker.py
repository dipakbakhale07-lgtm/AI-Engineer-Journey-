import json
import requests


with open("fact_checked_content.json", "r", encoding="utf-8") as file:
    drafts = json.load(file)


def revise_post(draft):
    prompt = f"""
You are a careful LinkedIn content editor.

SOURCE NOTES:
{draft["prompt"].split("SOURCE NOTES:")[1].split("AUDIENCE:")[0].strip()}

ORIGINAL POST:
{draft["generated_post"]}

FACT-CHECK RESULT:
{draft["fact_check"]}

Rewrite the post so that EVERY factual claim is supported by the SOURCE NOTES.

Rules:
1. Remove unsupported claims.
2. Remove invented achievements or results.
3. Do not invent numbers.
4. Do not invent personal experiences.
5. Do not invent technical definitions.
6. Keep the original topic and style.
7. Do not add information that is not in the source notes.
8. Do not use [FACT-CHECK NEEDED].
9. Do not use placeholders such as [KEY LESSON].
10. Keep the post natural for LinkedIn.

Return ONLY the final post.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:latest",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"]


for index, draft in enumerate(drafts, start=1):

    if "STATUS: NEEDS_REVIEW" in draft["fact_check"]:
        print(f"Revising {index}/9: {draft['topic']} - {draft['style']}")

        try:
            draft["revised_post"] = revise_post(draft)
            draft["final_status"] = "REVISED"

        except Exception as error:
            draft["revised_post"] = f"[REVISION ERROR] {error}"
            draft["final_status"] = "NEEDS_REVIEW"

    else:
        draft["revised_post"] = draft["generated_post"]
        draft["final_status"] = "PASS"


with open("revised_content.json", "w", encoding="utf-8") as file:
    json.dump(drafts, file, indent=4, ensure_ascii=False)


print()
print("Day 19 automatic revision completed.")
print("Saved to: revised_content.json")