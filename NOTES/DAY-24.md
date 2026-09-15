# DAY 24 — Build Tool 1 & Tool 2 Separately

## Goal

Build reliable Python tools before connecting them to an AI agent.

## Project

Project 4 — Multi-Tool Business Agent

## Tool 1 — FAQ Search

File:
tool_faq.py

Function:
search_faq(question)

Purpose:
Search sample FAQ knowledge and return a relevant answer.

Input:
question — string

Output:
Structured JSON response containing success status, question, answer, or error.

Example:
search_faq("What are your business hours?")

Result:
{
    "success": true,
    "question": "what are your business hours?",
    "answer": "Our business hours are 9:00 AM to 7:00 PM."
}

Missing input is handled safely with an error response.

## Tool 2 — Lead Search

File:
tool_leads.py

Function:
get_leads_by_status(status)

Purpose:
Find dummy leads based on their status.

Input:
status — string

Output:
Structured JSON response containing success status, requested status, count, matching leads, or error.

Example:
get_leads_by_status("interested")

Result:
Returns the matching interested leads and their details.

Missing input is handled safely with an error response.

## Independent Testing

Both tools were tested separately without using an AI agent.

Tool 1 tests:
- Business hours
- Home delivery
- Payment methods
- Return policy
- Missing question

Tool 2 tests:
- Interested leads
- New leads
- Qualified leads
- Contacted leads
- Missing status

## Key Learning

Reliable tools should be built and tested independently before connecting them to an AI agent.

Each tool should have:
- Clear inputs
- Clear outputs
- Structured responses
- Missing-input handling
- Independent testing

## Day 24 Deliverables

- [x] Tool 1 built
- [x] Tool 2 built
- [x] Both tools independently tested
- [x] Structured JSON responses
- [x] Missing input handled