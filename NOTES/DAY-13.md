# Day 13 — Connect Lead Input to AI

## Objective

Build a lead-processing system that accepts lead information, validates the input, sends it to the AI model, and returns a structured classification result.

## Implementation

The project is implemented using Python and local Ollama instead of an automation platform.

## Workflow

Lead Input
↓
Input Validation
↓
Ollama AI
↓
Lead Classification
↓
Structured JSON
↓
Final Result

## Features

- Accept new lead information through Python input.
- Validate required lead fields.
- Send validated lead data to the local Ollama model.
- Classify the lead into the required category.
- Determine lead priority.
- Generate a reason for the classification.
- Recommend the next action.
- Generate a draft reply.
- Return the AI result as structured JSON.

## Required Lead Fields

- Name
- Course Interest
- Lead Message
- City
- Timeline

## AI Output

The AI returns:

- category
- priority
- reason
- recommended_next_action
- draft_reply

## Testing

A new lead was entered through the Python program.

The system successfully:

1. Accepted the lead.
2. Validated the required fields.
3. Sent the lead to Ollama.
4. Classified the lead.
5. Generated the required AI information.
6. Displayed the structured JSON result.

## Final Result

Day 13 coding implementation was successfully completed and tested.

The project keeps the same core objective as the Builder Journey project while using a Python-based implementation instead of an automation workflow.