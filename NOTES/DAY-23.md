# DAY 23 — Project 4: Understand Tool-Using Agents

## Goal

Understand how an AI agent can move beyond a fixed script and make controlled decisions about which tool to use.

## Agent Loop

Goal
→ Choose Tool
→ Execute
→ Observe
→ Answer

## Tools

### 1. search_faq(question)

Purpose:
Search frequently asked questions and return the relevant answer.

Input:
question — string

Returns:
Relevant FAQ answer.

### 2. get_leads_by_status(status)

Purpose:
Find leads based on their current status.

Input:
status — string

Returns:
List of matching leads.

### 3. draft_followup(name, lead_status, interest)

Purpose:
Create a follow-up message for a lead.

Inputs:
name — string
lead_status — string
interest — string

Returns:
Follow-up message draft.

## Fixed Script vs Tool-Using Agent

A fixed script follows a predetermined sequence of steps.

A tool-using agent understands the user's goal and chooses the appropriate available tool.

## Routing Examples

1. Business hours → search_faq()
2. Home delivery → search_faq()
3. Payment methods → search_faq()
4. Interested leads → get_leads_by_status()
5. New leads → get_leads_by_status()
6. Qualified leads → get_leads_by_status()
7. Follow-up for Rahul → draft_followup()
8. Message for Priya → draft_followup()
9. Follow-up for Amit → draft_followup()
10. Follow-up for an interested lead → draft_followup()

## Architecture

User Request
↓
Agent
↓
Understand Goal
↓
Choose Tool
↓
Execute Tool
↓
Observe Result
↓
Final Answer

## Key Learning

An agent is different from a fixed script because it can select an appropriate tool based on the user's goal.

## Day 23 Deliverables

- [x] 3 tool definitions
- [x] Tool inputs and outputs
- [x] 10 routing examples
- [x] Agent architecture
- [x] Fixed script vs agent understanding