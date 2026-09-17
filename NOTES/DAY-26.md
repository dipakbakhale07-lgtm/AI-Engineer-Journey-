
# DAY 26 — Add a Third Tool + Multi-Step Task

## Goal

Handle a task that requires more than one tool action.

## Project

Project 4 — Multi-Tool Business Agent

## Third Tool

Function:
`generate_followup_draft(name, lead_status, interest)`

Purpose:
Generate a follow-up message draft.

The tool is draft-only and does not send messages.

## Multi-Step Task

Request:

"Show warm leads and prepare a follow-up draft for one."

## Warm Lead Mapping

Warm leads are mapped to:

`interested`

## Agent Sequence

Step 1:
`get_leads_by_status("interested")`

Result:
2 interested leads returned:
- Priya
- Sneha

Step 2:
Priya was selected from the returned lead data.

Priya details:
- Status: interested
- Interest: chatbot

Step 3:
`generate_followup_draft()`

Arguments:
- Name: Priya
- Status: interested
- Interest: chatbot

Result:
Follow-up draft generated successfully.

## Tool Sequence

`get_leads_by_status`
↓
`generate_followup_draft`

## Tool-Call Control

Maximum tool calls:
3

Actual tool calls:
2

## Safety

The follow-up functionality is draft-only.

No message was sent.

No irreversible action was performed.

## JSON Response Handling

The agent includes controlled JSON parsing so the Ollama response can be extracted safely even when the model produces additional text around the JSON object.

## Logging

The agent logs:
- Tool-call step
- Request
- Selected tool
- Arguments
- Tool output
- Tool sequence
- Number of tool calls
- Maximum tool-call limit
- Final result

## Key Learning

A multi-step agent can use the output of one tool as the input for another tool.

The agent can therefore move from:

Find leads
↓
Select a lead
↓
Generate a follow-up draft

while keeping execution controlled.

## Day 26 Deliverables

- [x] Third tool added
- [x] Multi-step task completed
- [x] Two tool calls executed
- [x] Tool-call sequence logged
- [x] Maximum tool-call limit added
- [x] Draft-only action maintained
- [x] No irreversible action performed

## STATUS

Completed