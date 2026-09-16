# DAY 26 — Add a Third Tool + Multi-Step Task

## Goal

Handle a small task that requires more than one action.

## Project

Project 4 — Multi-Tool Business Agent

## Third Tool

Function:
`generate_followup_draft(name, lead_status, interest)`

Purpose:
Generate a follow-up message draft for a selected lead.

The tool is draft-only and does not send messages.

## Multi-Step Task

Request:

"Show interested leads and prepare a follow-up draft for Priya."

## Agent Sequence

Step 1:
`get_leads_by_status("interested")`

Result:
Two interested leads were returned:
- Priya
- Sneha

Step 2:
Priya was identified from the returned lead data.

Step 3:
`generate_followup_draft()` was executed using Priya's details.

Result:
A follow-up draft was successfully generated.

## Tool Sequence

`get_leads_by_status`
↓
`generate_followup_draft`

## Tool-Call Control

Maximum tool calls:
3

Actual tool calls used:
2

This keeps the multi-step task controlled.

## Safety

The follow-up functionality is draft-only.

No message is sent and no irreversible action is performed.

## Logging

The agent logs:

- Each tool call
- Tool-call step number
- Request
- Selected tool
- Arguments
- Output
- Final multi-step result
- Number of tool calls used
- Maximum tool-call limit
- Tool-call sequence

## Key Learning

A multi-step agent can use the output of one tool to determine the input for the next tool.

Controlled tool limits help prevent uncontrolled execution.

## Day 26 Deliverables

- [x] Third tool added
- [x] Multi-step task completed
- [x] Tool-call sequence logged
- [x] Maximum tool-call limit added
- [x] Draft-only action maintained
- [x] No irreversible action performed