
# DAY 25 — Connect the Agent to Tools

## Goal

Allow the AI agent to select and execute the correct Python tool.

## Project

Project 4 — Multi-Tool Business Agent

## AI Model

Ollama — llama3:latest

## Connected Tools

### Tool 1 — FAQ Search

Function:
`search_faq(question)`

Purpose:
Answer business FAQ questions.

### Tool 2 — Lead Search

Function:
`get_leads_by_status(status)`

Purpose:
Find leads by status:
- new
- interested
- qualified
- contacted

Warm leads are mapped to:
`interested`

### Tool 3 — Follow-up Draft

Function:
`generate_followup_draft(name, lead_status, interest)`

Purpose:
Generate a follow-up draft.

Important:
This tool only creates a draft.
It does not send messages.

## Agent Flow

User Request
↓
Ollama Tool Selection
↓
Argument Generation
↓
Argument Normalization
↓
Python Tool Execution
↓
Structured Output

## Day 25 Tests

Six single-tool requests were tested.

1. Business hours
Expected: `search_faq`
Selected: `search_faq`
Result: PASS

2. Home delivery
Expected: `search_faq`
Selected: `search_faq`
Result: PASS

3. Interested leads
Expected: `get_leads_by_status`
Selected: `get_leads_by_status`
Argument: `status="interested"`
Result: PASS

4. Qualified leads
Expected: `get_leads_by_status`
Selected: `get_leads_by_status`
Argument: `status="qualified"`
Result: PASS

5. Payment methods
Expected: `search_faq`
Selected: `search_faq`
Result: PASS

6. Follow-up draft for Priya
Expected: `generate_followup_draft`
Selected: `generate_followup_draft`
Result: PASS

## Final Result

6/6 correct tool selections and successful executions.

Accuracy:
100%

## Logging

Tool executions are recorded in:

`agent_tool_log.jsonl`

The log contains:
- Timestamp
- Request
- Selected tool
- Arguments
- Tool output

## Key Learning

An AI agent can use an LLM to understand a request, select a suitable tool, provide arguments, execute the Python function, and observe the structured result.

## Day 25 Deliverables

- [x] Agent connected to Python tools
- [x] Ollama model connected
- [x] Tool descriptions defined
- [x] Six single-tool requests tested
- [x] 6/6 successful
- [x] Tool execution verified
- [x] Tool output logged

## STATUS

COMPLETE
