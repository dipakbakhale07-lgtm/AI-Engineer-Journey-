
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
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(entry) + "\n")
    except Exception as error:
        print(f"Logging error: {error}")


def tool_catalog():
    return json.dumps(TOOLS, indent=2)


def ask_ollama(messages):
    try:
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

        if "message" not in data:
            raise ValueError("Ollama returned an invalid response.")

        if "content" not in data["message"]:
            raise ValueError(
                "Ollama response does not contain message content."
            )

        return data["message"]["content"]

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Ollama is not running or is unavailable at localhost:11434."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Ollama request timed out."
        )

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Ollama API returned an HTTP error: {error}"
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Ollama request failed: {error}"
        )

    except (ValueError, KeyError, TypeError) as error:
        raise RuntimeError(
            f"Invalid response from Ollama: {error}"
        )


def parse_json(text):
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "", 1)
        text = text.strip()

    start = text.find("{")

    if start == -1:
        raise ValueError("Model did not return JSON.")

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

    raise ValueError("Model returned incomplete JSON.")


def normalize_arguments(tool_name, arguments):
    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be a JSON object.")

    if tool_name == "get_leads_by_status":
        status = str(arguments.get("status", "")).strip().lower()

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
    arguments = result.get("arguments", {})

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
        result = PYTHON_TOOLS[tool_name](**arguments)

        if not isinstance(result, dict):
            return {
                "success": False,
                "error": "Tool returned an invalid response format."
            }

        return result

    except TypeError as error:
        return {
            "success": False,
            "error": f"Invalid tool arguments: {error}"
        }

    except Exception as error:
        return {
            "success": False,
            "error": f"Tool execution failed: {error}"
        }


def run_single_test(request):
    print("=" * 70)
    print("DAY 25 TEST")
    print(f"Request: {request}")
    print()

    try:
        tool_name, arguments = select_tool(request)

        print(f"Model selected tool: {tool_name}")
        print(f"Arguments: {json.dumps(arguments)}")

        result = execute_tool(
            tool_name,
            arguments
        )

        print("Tool output:")
        print(json.dumps(result, indent=2))

        if not result.get("success", False):
            print()
            print("CLEAR FAILURE RESPONSE:")
            print(
                f"The requested tool could not be completed. "
                f"Reason: {result.get('error', 'Unknown error.')}"
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
        print()

        print("CLEAR FAILURE RESPONSE:")
        print(
            f"The agent could not complete the request. "
            f"Reason: {error}"
        )

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
    request = "Show warm leads and prepare a follow-up draft for one."

    print("=" * 70)
    print("DAY 26 MULTI-STEP TASK")
    print(f"Request: {request}")
    print(f"Maximum tool calls: {MAX_TOOL_CALLS}")
    print()

    tool_calls = 0
    sequence = []

    try:
        # STEP 1: Find warm leads.
        tool_calls += 1

        tool_name = "get_leads_by_status"
        arguments = {
            "status": "interested"
        }

        sequence.append(tool_name)

        print(f"Step {tool_calls}: {tool_name}")
        print(f"Arguments: {json.dumps(arguments)}")

        result = execute_tool(
            tool_name,
            arguments
        )

        print("Tool output:")
        print(json.dumps(result, indent=2))
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

        if not result.get("success", False):
            raise RuntimeError(
                f"Lead lookup failed: {result.get('error')}"
            )

        leads = result.get("leads", [])

        if not leads:
            raise RuntimeError(
                "No warm leads were found."
            )

        # STEP 2: Prepare a draft for the first lead.
        selected_lead = leads[0]

        tool_calls += 1

        tool_name = "generate_followup_draft"

        arguments = {
            "name": selected_lead["name"],
            "lead_status": selected_lead["status"],
            "interest": selected_lead["interest"]
        }

        sequence.append(tool_name)

        print(f"Step {tool_calls}: {tool_name}")
        print(f"Arguments: {json.dumps(arguments)}")

        result = execute_tool(
            tool_name,
            arguments
        )

        print("Tool output:")
        print(json.dumps(result, indent=2))
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

        if not result.get("success", False):
            raise RuntimeError(
                f"Follow-up draft failed: {result.get('error')}"
            )

        # FINAL RESPONSE.
        draft = result.get("draft")

        print("FINAL RESPONSE:")
        print({
            "success": True,
            "draft": draft
        })
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
            "answer": {
                "success": True,
                "draft": draft
            }
        })

    except Exception as error:
        print("ERROR:")
        print(str(error))
        print()

        print("CLEAR FAILURE RESPONSE:")
        print(
            f"The multi-step task could not be completed. "
            f"Reason: {error}"
        )

        write_log({
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "type": "day27_error",
            "request": request,
            "tool_calls_used": tool_calls,
            "maximum_tool_calls": MAX_TOOL_CALLS,
            "tool_sequence": sequence,
            "error": str(error)
        })


def run_day27_failed_tool_test():
    print("=" * 70)
    print("DAY 27 FAILED TOOL TEST")
    print()

    test_tool = "get_leads_by_status"
    test_arguments = {
        "status": ""
    }

    print(f"Test tool: {test_tool}")
    print(f"Arguments: {json.dumps(test_arguments)}")
    print()

    result = execute_tool(
        test_tool,
        test_arguments
    )

    print("Tool output:")
    print(json.dumps(result, indent=2))
    print()

    if result.get("success") is False:
        error_message = result.get(
            "error",
            "Unknown error."
        )

        print("FAILURE HANDLED CORRECTLY:")
        print(
            f"The requested tool could not be completed. "
            f"Reason: {error_message}"
        )

        write_log({
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "type": "day27_failed_tool_test",
            "tool": test_tool,
            "arguments": test_arguments,
            "result": result,
            "handled": True
        })

    else:
        print(
            "Unexpected result: failed-tool test did not fail."
        )

    print()


def main():
    print("PROJECT 4 — MULTI-TOOL BUSINESS AGENT")
    print(f"Model: {MODEL}")
    print(f"Maximum tool calls: {MAX_TOOL_CALLS}")
    print()

    print("DAY 25 — NORMAL TOOL TESTS")
    run_day25()

    print("DAY 26 — MULTI-STEP TEST")
    run_multi_step_task()

    print("DAY 27 — FAILED TOOL TEST")
    run_day27_failed_tool_test()


if __name__ == "__main__":
    main()
def run_day27_failed_tool_test():
    print("=" * 70)
    print("DAY 27 FAILED TOOL TEST")
    print()

    test_tool = "get_leads_by_status"
    test_arguments = {
        "status": ""
    }

    print(f"Test tool: {test_tool}")
    print(f"Arguments: {json.dumps(test_arguments)}")
    print()

    result = execute_tool(
        test_tool,
        test_arguments
    )

    print("Tool output:")
    print(json.dumps(result, indent=2))
    print()

    if result.get("success") is False:
        error_message = result.get(
            "error",
            "Unknown error."
        )

        print("FAILURE HANDLED CORRECTLY:")
        print(
            f"The requested tool could not be completed. "
            f"Reason: {error_message}"
        )

        write_log({
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "type": "day27_failed_tool_test",
            "tool": test_tool,
            "arguments": test_arguments,
            "result": result,
            "handled": True
        })

    else:
        print("Unexpected result: failed-tool test did not fail.")

    print()

