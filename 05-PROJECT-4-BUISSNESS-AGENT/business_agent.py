import json
import re
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
        "function": search_faq,
        "description": (
            "Search business FAQ information. "
            "Input: question (string). "
            "Use for business hours, home delivery, payment methods, "
            "return policy, and similar FAQ questions."
        )
    },
    "get_leads_by_status": {
        "function": get_leads_by_status,
        "description": (
            "Retrieve leads by status. "
            "Input: status (string). "
            "Valid statuses: new, interested, qualified, contacted. "
            "Warm leads mean interested leads."
        )
    },
    "generate_followup_draft": {
        "function": generate_followup_draft,
        "description": (
            "Generate a follow-up message draft. "
            "Inputs: name, lead_status, interest. "
            "This only creates a draft and never sends a message."
        )
    }
}


def log_event(event_type, data):
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "type": event_type,
        **data
    }

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def ask_ollama(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            raise ValueError(
                "Ollama returned an invalid response format."
            )

        message = data.get("message")

        if not isinstance(message, dict):
            raise ValueError(
                "Ollama response does not contain a valid message."
            )

        content = message.get("content", "")

        if not isinstance(content, str) or not content.strip():
            raise ValueError(
                "Ollama returned an empty response."
            )

        return content.strip()

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Cannot connect to Ollama. Make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Ollama request timed out."
        )

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Ollama HTTP error: {error}"
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Ollama request failed: {error}"
        )

    except ValueError:
        raise

    except Exception as error:
        raise RuntimeError(
            f"Ollama error: {error}"
        )


def extract_json(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("No JSON response received.")

    text = text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    cleaned = re.sub(
        r"```(?:json)?",
        "",
        text,
        flags=re.IGNORECASE
    ).replace("```", "").strip()

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:
        pass

    object_start = cleaned.find("{")
    array_start = cleaned.find("[")

    starts = []

    if object_start >= 0:
        starts.append((object_start, "{"))

    if array_start >= 0:
        starts.append((array_start, "["))

    if not starts:
        raise ValueError("No JSON object found.")

    start, opening = min(
        starts,
        key=lambda item: item[0]
    )

    closing = "}" if opening == "{" else "]"

    depth = 0
    in_string = False
    escape = False

    for index in range(start, len(cleaned)):
        char = cleaned[index]

        if in_string:

            if escape:
                escape = False

            elif char == "\\":
                escape = True

            elif char == '"':
                in_string = False

            continue

        if char == '"':
            in_string = True
            continue

        if char == opening:
            depth += 1

        elif char == closing:
            depth -= 1

            if depth == 0:
                candidate = cleaned[
                    start:index + 1
                ]

                try:
                    return json.loads(candidate)

                except json.JSONDecodeError:
                    break

    raise ValueError(
        "No valid JSON object found."
    )


def normalize_arguments(tool_name, arguments, request):

    if not isinstance(arguments, dict):
        arguments = {}

    request = request.strip()
    request_lower = request.lower()

    # ---------------------------------------------------------
    # TOOL 1 — FAQ
    # ---------------------------------------------------------

    if tool_name == "search_faq":

        question = arguments.get(
            "question",
            ""
        )

        if (
            not isinstance(question, str)
            or not question.strip()
        ):
            arguments["question"] = request

    # ---------------------------------------------------------
    # TOOL 2 — LEADS
    # ---------------------------------------------------------

    elif tool_name == "get_leads_by_status":

        status = arguments.get(
            "status",
            ""
        )

        if not isinstance(status, str):
            status = ""

        status = status.strip().lower()

        if status in ("warm", "hot"):
            status = "interested"

        if not status:

            if "qualified" in request_lower:
                status = "qualified"

            elif "interested" in request_lower:
                status = "interested"

            elif (
                "warm" in request_lower
                or "hot" in request_lower
            ):
                status = "interested"

            elif "contacted" in request_lower:
                status = "contacted"

            elif "new" in request_lower:
                status = "new"

        arguments["status"] = status

    # ---------------------------------------------------------
    # TOOL 3 — FOLLOW-UP DRAFT
    # ---------------------------------------------------------

    elif tool_name == "generate_followup_draft":

        name = arguments.get(
            "name",
            ""
        )

        lead_status = arguments.get(
            "lead_status",
            ""
        )

        interest = arguments.get(
            "interest",
            ""
        )

        if not isinstance(name, str):
            name = ""

        if not isinstance(lead_status, str):
            lead_status = ""

        if not isinstance(interest, str):
            interest = ""

        # Known Project 4 leads.
        known_leads = {
            "Priya": {
                "status": "interested",
                "interest": "chatbot"
            },
            "Amit": {
                "status": "qualified",
                "interest": "RAG system"
            },
            "Rahul": {
                "status": "new",
                "interest": "AI automation"
            },
            "Sneha": {
                "status": "interested",
                "interest": "AI content"
            },
            "Vikram": {
                "status": "contacted",
                "interest": "AI agents"
            }
        }

        # Detect lead name from request.
        if not name.strip():

            for lead_name in known_leads:

                if lead_name.lower() in request_lower:
                    name = lead_name
                    break

        name = name.strip()

        # Use the known lead record.
        if name in known_leads:

            lead_data = known_leads[name]

            if not lead_status.strip():
                lead_status = lead_data["status"]

            if not interest.strip():
                interest = lead_data["interest"]

        # Fallback status detection.
        if not lead_status.strip():

            if "qualified" in request_lower:
                lead_status = "qualified"

            elif (
                "interested" in request_lower
                or "warm" in request_lower
            ):
                lead_status = "interested"

            elif "contacted" in request_lower:
                lead_status = "contacted"

            elif "new" in request_lower:
                lead_status = "new"

        if not interest.strip():
            interest = "your enquiry"

        arguments["name"] = name

        arguments["lead_status"] = (
            lead_status.strip().lower()
        )

        arguments["interest"] = (
            interest.strip()
        )

    return arguments


def select_tool(request):

    tool_descriptions = "\n".join(
        f"- {name}: {data['description']}"
        for name, data in TOOLS.items()
    )

    system_message = f"""
You are a controlled business agent.

Choose exactly ONE tool for the user's request.

Available tools:
{tool_descriptions}

Rules:
- Return ONLY one JSON object.
- Never return a JSON array.
- The JSON format must be:
  {{
    "tool": "tool_name",
    "arguments": {{}}
  }}
- Do not execute tools yourself.
- Do not invent tool names.
- For FAQ questions, select search_faq.
- For lead-status requests, select get_leads_by_status.
- If the user says warm leads, use get_leads_by_status with status "interested".
- For follow-up requests, select generate_followup_draft.
- Keep arguments as a JSON object.
"""

    content = ask_ollama(
        [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": request
            }
        ]
    )

    selection = extract_json(content)

    if isinstance(selection, list):

        if (
            len(selection) == 1
            and isinstance(selection[0], dict)
        ):
            selection = selection[0]

        else:
            raise ValueError(
                "Invalid tool selection format. "
                "Expected one JSON object."
            )

    if not isinstance(selection, dict):
        raise ValueError(
            "Invalid tool selection format. "
            "Expected a JSON object."
        )

    tool_name = selection.get("tool")

    if (
        not isinstance(tool_name, str)
        or not tool_name.strip()
    ):
        raise ValueError(
            "No tool was selected."
        )

    tool_name = tool_name.strip()

    arguments = selection.get(
        "arguments",
        {}
    )

    arguments = normalize_arguments(
        tool_name,
        arguments,
        request
    )

    if tool_name not in TOOLS:
        raise ValueError(
            f"Invalid tool selected: {tool_name}"
        )

    return tool_name, arguments


def execute_tool(tool_name, arguments):

    try:

        if tool_name not in TOOLS:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

        if not isinstance(arguments, dict):
            return {
                "success": False,
                "error": (
                    "Tool arguments must be "
                    "a JSON object."
                )
            }

        function = TOOLS[tool_name]["function"]

        result = function(**arguments)

        if not isinstance(result, dict):
            return {
                "success": False,
                "error": (
                    "Tool returned an invalid result."
                )
            }

        return result

    except TypeError as error:

        return {
            "success": False,
            "error": (
                f"Invalid tool arguments: {error}"
            )
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


def run_single_test(request):

    try:

        tool_name, arguments = select_tool(
            request
        )

        result = execute_tool(
            tool_name,
            arguments
        )

        log_event(
            "single_tool_request",
            {
                "request": request,
                "selected_tool": tool_name,
                "arguments": arguments,
                "result": result
            }
        )

        if result.get("success") is False:

            print(
                "ERROR: "
                f"{result.get('error', 'Tool failed.')}"
            )

            return False

        print(
            f"TOOL: {tool_name}"
        )

        print(
            json.dumps(
                result,
                indent=2
            )
        )

        return True

    except Exception as error:

        log_event(
            "single_tool_error",
            {
                "request": request,
                "error": str(error)
            }
        )

        print(
            f"ERROR: {error}"
        )

        return False


def run_day25():

    print(
        "DAY 25 — NORMAL TOOL TESTS"
    )

    requests_to_test = [
        "What are your business hours?",
        "Do you provide home delivery?",
        "Show interested leads",
        "Show qualified leads",
        "What payment methods do you accept?",
        "Create a follow-up draft for Priya"
    ]

    successful = 0

    for number, request in enumerate(
        requests_to_test,
        start=1
    ):

        print()
        print(
            f"{number}. {request}"
        )

        if run_single_test(request):
            successful += 1

    print()

    print(
        f"DAY 25 RESULT: "
        f"{successful}/{len(requests_to_test)} successful"
    )

    return successful


def run_multi_step_task():

    print("=" * 70)
    print(
        "DAY 26 — MULTI-STEP TEST"
    )
    print("=" * 70)

    request = (
        "Show warm leads and prepare "
        "a follow-up draft for one."
    )

    print(
        f"Request: {request}"
    )
    print()

    tool_call_count = 0

    # STEP 1
    tool_call_count += 1

    if tool_call_count > MAX_TOOL_CALLS:

        return {
            "success": False,
            "error": (
                "Maximum tool-call limit reached."
            )
        }

    tool1 = "get_leads_by_status"

    args1 = {
        "status": "interested"
    }

    result1 = execute_tool(
        tool1,
        args1
    )

    log_event(
        "multi_step_tool_call",
        {
            "request": request,
            "step": 1,
            "selected_tool": tool1,
            "arguments": args1,
            "result": result1
        }
    )

    print(
        "Step 1: get_leads_by_status"
    )

    print(
        json.dumps(
            result1,
            indent=2
        )
    )

    print()

    if not result1.get("success"):

        return {
            "success": False,
            "error": result1.get(
                "error",
                "Step 1 failed."
            )
        }

    leads = result1.get(
        "leads",
        []
    )

    if not leads:

        return {
            "success": False,
            "error": (
                "No warm/interested leads found."
            )
        }

    selected_lead = leads[0]

    # STEP 2
    tool_call_count += 1

    if tool_call_count > MAX_TOOL_CALLS:

        return {
            "success": False,
            "error": (
                "Maximum tool-call limit reached."
            )
        }

    tool2 = (
        "generate_followup_draft"
    )

    args2 = {
        "name": selected_lead["name"],
        "lead_status": selected_lead["status"],
        "interest": selected_lead["interest"]
    }

    result2 = execute_tool(
        tool2,
        args2
    )

    log_event(
        "multi_step_tool_call",
        {
            "request": request,
            "step": 2,
            "selected_tool": tool2,
            "arguments": args2,
            "result": result2
        }
    )

    print(
        "Step 2: generate_followup_draft"
    )

    print(
        json.dumps(
            result2,
            indent=2
        )
    )

    print()

    if not result2.get("success"):

        return {
            "success": False,
            "error": result2.get(
                "error",
                "Step 2 failed."
            )
        }

    final_response = {
        "success": True,
        "draft": result2["draft"]
    }

    print(
        "FINAL RESPONSE:"
    )

    print(
        final_response
    )

    print()

    return final_response


def run_day27_failed_tool_test():

    print("=" * 70)
    print(
        "DAY 27 — FAILED TOOL TEST"
    )
    print("=" * 70)

    tool_name = (
        "get_leads_by_status"
    )

    arguments = {
        "status": ""
    }

    result = execute_tool(
        tool_name,
        arguments
    )

    log_event(
        "day27_failed_tool_test",
        {
            "selected_tool": tool_name,
            "arguments": arguments,
            "result": result
        }
    )

    print()
    print("Tool output:")

    print(
        json.dumps(
            result,
            indent=2
        )
    )

    print()

    if result.get("success") is False:

        print(
            "FAILURE HANDLED CORRECTLY:"
        )

        print(
            "The requested tool could not "
            "be completed. "
            f"Reason: {result.get('error')}"
        )

    else:

        print(
            "FAILED TEST DID NOT FAIL "
            "AS EXPECTED."
        )

    print()

    return result


def run_agent_request(request):

    if (
        not isinstance(request, str)
        or not request.strip()
    ):

        return {
            "success": False,
            "error": "Request is required."
        }

    request = request.strip()

    try:

        tool_name, arguments = select_tool(
            request
        )

        log_event(
            "agent_request",
            {
                "request": request,
                "selected_tool": tool_name,
                "arguments": arguments
            }
        )

        result = execute_tool(
            tool_name,
            arguments
        )

        log_event(
            "agent_result",
            {
                "request": request,
                "selected_tool": tool_name,
                "arguments": arguments,
                "result": result
            }
        )

        if result.get("success") is False:

            return {
                "success": False,
                "tool": tool_name,
                "error": result.get(
                    "error",
                    "The tool could not "
                    "complete the request."
                )
            }

        return {
            "success": True,
            "tool": tool_name,
            "arguments": arguments,
            "result": result
        }

    except Exception as error:

        log_event(
            "agent_error",
            {
                "request": request,
                "error": str(error)
            }
        )

        return {
            "success": False,
            "error": str(error)
        }


def main():

    print(
        "PROJECT 4 — MULTI-TOOL BUSINESS AGENT"
    )

    print(
        f"Model: {MODEL}"
    )

    print(
        f"Maximum tool calls: "
        f"{MAX_TOOL_CALLS}"
    )

    print()

    day25_success = run_day25()

    print()

    run_multi_step_task()

    print()

    run_day27_failed_tool_test()

    print()

    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    print(
        f"Day 25: "
        f"{day25_success}/6 successful"
    )

    print(
        "Day 26: multi-step task executed"
    )

    print(
        "Day 27: failed-tool handling tested"
    )


if __name__ == "__main__":
    main()