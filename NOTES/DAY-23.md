# DAY 23 — Understand Tool-Using Agents

## Goal

Understand how an AI agent can choose and use different tools based on the user's request.

## Agent Loop

User Goal
↓
Understand Request
↓
Choose Tool
↓
Execute Tool
↓
Observe Result
↓
Final Answer

## Tool 1 — search_faq()

### Purpose
Search frequently asked questions and return the relevant answer.

### Input
question: string

### Example
search_faq("What are your business hours?")

### Return
A relevant FAQ answer as a string.

---

## Tool 2 — get_leads_by_status()

### Purpose
Find leads based on their current status.

### Input
status: string

### Example
get_leads_by_status("interested")

### Return
A list of leads matching the requested status.

---

## Tool 3 — draft_followup()

### Purpose
Create a follow-up message for a lead.

### Input
name: string
lead_status: string
interest: string

### Example
draft_followup("Rahul", "interested", "AI automation")

### Return
A draft follow-up message as a string.

---

## Fixed Script vs Agent

### Fixed Script
The developer decides the sequence of actions in advance.

Example:

User Request
↓
Always run Tool 1
↓
Always run Tool 2
↓
Return Result

### Tool-Using Agent
The system understands the user's request and chooses the appropriate tool.

Example:

User Request
↓
Understand Goal
↓
Choose Tool
↓
Execute Tool
↓
Observe Result
↓
Answer

## Key Learning

A fixed script follows a predetermined workflow.

A tool-using agent makes a controlled decision about which available tool should be used for the user's request.

## Day 23 Deliverables

- 3 tool definitions
- Tool inputs and outputs
- 10 routing examples
- Agent architecture