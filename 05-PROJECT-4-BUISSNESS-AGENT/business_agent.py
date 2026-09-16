import json
from datetime import datetime

import requests

from tool_faq import search_faq
from tool_leads import get_leads_by_status
from tool_followup import generate_followup_draft


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3:latest"

MAX_TOOL_CALLS = 3
LOG_FILE = "agent_tool_log.jsonl"


TOOLS = {
    "search_faq": {
        "description": (
            "Answer business FAQ questions about business hours, "
            "home delivery, payment methods, and return policy."
        ),
        "parameters": {
            "question": "The user's business FAQ question."
        }
    },

    "get_leads_by_status": {
        "description": (
            "Find business leads by status. "
            "Stored statuses are new, interested, qualified, and contacted. "
            "If the user says warm leads, use status='interested'."
        ),
        "parameters": {
            "status": (
                "Lead status. Use only: new, interested, "
                "qualified, or contacted."
            )
        }
    },

    "generate_followup_draft": {
        "description": (
            "Create a follow-up message draft using the lead's name, "
            "status, and interest. This tool only creates a draft "
            "and never sends messages."
        ),
        "parameters": {
            "name": "Lead name.",
            "lead_status": "Lead status.",
            "interest": "What the lead is interested in."
        }
    }
}


PYTHON_TOOLS = {
    "search_faq": search_faq,
    "get_leads_by_status": get_leads_by_status,
    "generate_followup_draft": generate_followup_draft
}


def write_log(entry):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(entry) + "\n")


def tool_catalog():
    return json.dumps(TOOLS, indent=2)


def ask_ollama(messages):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "temperature": 0
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


def parse_json(text):
    """
    Extract the first complete JSON object from the model response.

    This prevents errors when Llama returns extra text or
    multiple JSON objects.
    """

    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "", 1)
        text = text.strip()

    start = text.find("{")

    if start == -1:
        raise ValueError(
            "Model did not return JSON."
        )

    depth = 0
    in_string = False
    escape = False

    for index in range(start, len(text)):

        character = text[index]

        if escape:
            escape = False
            continue

        if character == "\\" and in_string:
            escape = True
            continue

        if character == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if character == "{":
            depth += 1

        elif character == "}":
            depth -= 1

            if depth == 0:
                json_text = text[start:index + 1]
                return json.loads(json_text)

    raise ValueError(
        "Model returned incomplete JSON."
    )


def normalize_arguments(tool_name, arguments):

    if tool_name == "get_leads_by_status":

        status = arguments.get(
            "status",
            ""
        ).strip().lower()

        status_map = {
            "warm": "interested",
            "hot": "interested",
            "new": "new",
            "interested": "interested",
            "qualified": "qualified",
            "contacted": "contacted"
        }

        if status in status_map:
            arguments["status"] = status_map[status]

    return arguments


def select_tool(request):

    system_prompt = f"""
You are a controlled business-agent router.

Available tools:

{tool_catalog()}

User request:
{request}

Select exactly ONE appropriate tool.

Return ONLY one valid JSON object:

{{
    "tool": "tool_name",
    "arguments": {{}}
}}

Rules:
- Do not invent tool names.
- Use only the available tools.
- For warm leads, use status="interested".
- For interested leads, use status="interested".
- For qualified leads, use status="qualified".
- For new leads, use status="new".
- For contacted leads, use status="contacted".
- For FAQ questions, pass the user's question.
- For a follow-up draft for Priya, use:
  name="Priya"
  lead_status="interested"
  interest="chatbot"
"""

    raw_response = ask_ollama([
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": request
        }
    ])

    result = parse_json(raw_response)

    tool_name = result.get("tool")
    arguments = result.get(
        "arguments",
        {}
    )

    if tool_name not in PYTHON_TOOLS:
        raise ValueError(
            f"Invalid tool selected: {tool_name}"
        )

    arguments = normalize_arguments(
        tool_name,
        arguments
    )

    return tool_name, arguments


def execute_tool(tool_name, arguments):

    if tool_name not in PYTHON_TOOLS:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    try:
        return PYTHON_TOOLS[tool_name](**arguments)

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


def run_single_test(request):

    print("=" * 70)
    print("DAY 25 TEST")
    print(f"Request: {request}")
    print()

    try:

        tool_name, arguments = select_tool(request)

        print(
            f"Model selected tool: {tool_name}"
        )

        print(
            f"Arguments: {json.dumps(arguments)}"
        )

        result = execute_tool(
            tool_name,
            arguments
        )

        print("Tool output:")

        print(
            json.dumps(
                result,
                indent=2
            )
        )

        write_log({
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "type": "day25_single_tool",
            "request": request,
            "selected_tool": tool_name,
            "arguments": arguments,
            "output": result
        })

    except Exception as error:

        print("ERROR:")
        print(str(error))

        write_log({
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "type": "day25_error",
            "request": request,
            "error": str(error)
        })

    print()


def run_day25():

    tests = [
        "What are your business hours?",
        "Do you provide home delivery?",
        "Show interested leads.",
        "Show qualified leads.",
        "What payment methods do you accept?",
        "Prepare a follow-up draft for Priya."
    ]

    for request in tests:
        run_single_test(request)


def run_multi_step_task():

    request = (
        "Show warm leads and prepare a follow-up draft for one."
    )

    print("=" * 70)
    print("DAY 26 MULTI-STEP TASK")
    print(f"Request: {request}")
    print(
        f"Maximum tool calls: {MAX_TOOL_CALLS}"
    )
    print()

    messages = [
        {
            "role": "system",
            "content": f"""
You are a controlled business agent.

Available tools:

{tool_catalog()}

Task:
Show warm leads and prepare a follow-up draft for one.

Rules:
- Warm leads means interested leads.
- Therefore use status="interested".
- First find the interested leads.
- Select one lead from the returned results.
- Then generate a follow-up draft for that lead.
- The follow-up must remain a draft.
- Never send a message.
- Never perform an irreversible action.
- Maximum tool calls: {MAX_TOOL_CALLS}.

Return ONLY ONE JSON OBJECT.

For a tool action:

{{
    "action": "tool",
    "tool": "tool_name",
    "arguments": {{}}
}}

For the completed task:

{{
    "action": "final",
    "answer": "..."
}}
"""
        },
        {
            "role": "user",
            "content": request
        }
    ]

    tool_calls = 0
    sequence = []

    while tool_calls < MAX_TOOL_CALLS:

        try:

            raw_response = ask_ollama(messages)

            decision = parse_json(
                raw_response
            )

            action = decision.get(
                "action"
            )

            if action == "final":

                answer = decision.get(
                    "answer",
                    "Task completed."
                )

                print("FINAL RESPONSE:")
                print(answer)
                print()

                write_log({
                    "timestamp": datetime.now().isoformat(
                        timespec="seconds"
                    ),
                    "type": "day26_final",
                    "request": request,
                    "tool_calls_used": tool_calls,
                    "maximum_tool_calls": MAX_TOOL_CALLS,
                    "tool_sequence": sequence,
                    "answer": answer
                })

                return

            if action != "tool":
                raise ValueError(
                    "Model returned an invalid action."
                )

            tool_name = decision.get(
                "tool"
            )

            arguments = decision.get(
                "arguments",
                {}
            )

            if tool_name not in PYTHON_TOOLS:
                raise ValueError(
                    f"Invalid tool selected: {tool_name}"
                )

            arguments = normalize_arguments(
                tool_name,
                arguments
            )

            tool_calls += 1

            sequence.append(
                tool_name
            )

            print(
                f"Step {tool_calls}: {tool_name}"
            )

            print(
                f"Arguments: {json.dumps(arguments)}"
            )

            result = execute_tool(
                tool_name,
                arguments
            )

            print("Tool output:")

            print(
                json.dumps(
                    result,
                    indent=2
                )
            )

            print()

            write_log({
                "timestamp": datetime.now().isoformat(
                    timespec="seconds"
                ),
                "type": "day26_tool_call",
                "step": tool_calls,
                "request": request,
                "selected_tool": tool_name,
                "arguments": arguments,
                "output": result
            })

            messages.append({
                "role": "assistant",
                "content": json.dumps(
                    decision
                )
            })

            messages.append({
                "role": "user",
                "content": (
                    "Tool result:\n"
                    f"{json.dumps(result)}\n\n"
                    "Continue the task. "
                    "Use another tool if required. "
                    "Otherwise return the final JSON object."
                )
            })

        except Exception as error:

            print("ERROR:")
            print(str(error))

            write_log({
                "timestamp": datetime.now().isoformat(
                    timespec="seconds"
                ),
                "type": "day26_error",
                "request": request,
                "tool_calls_used": tool_calls,
                "maximum_tool_calls": MAX_TOOL_CALLS,
                "tool_sequence": sequence,
                "error": str(error)
            })

            return

    print(
        "Maximum tool-call limit reached."
    )

    print(
        f"Tool calls used: {tool_calls}"
    )

    write_log({
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "type": "day26_limit",
        "request": request,
        "tool_calls_used": tool_calls,
        "maximum_tool_calls": MAX_TOOL_CALLS,
        "tool_sequence": sequence
    })


def main():

    print(
        "PROJECT 4 — MULTI-TOOL BUSINESS AGENT"
    )

    print(
        f"Model: {MODEL}"
    )

    print()

    run_day25()

    print()

    run_multi_step_task()


if __name__ == "__main__":
    main()