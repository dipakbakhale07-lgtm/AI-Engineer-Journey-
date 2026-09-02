# Day 12 — Create the Classification Prompt

## Goal

Make the LLM produce predictable and structured lead classification results.

## What I Learned

Today I learned how prompt engineering can be used to make an LLM return structured and consistent results.

A classification prompt should clearly define:

- The role of the AI.
- What task it needs to perform.
- Available categories.
- Priority levels.
- Classification rules.
- Restrictions on unsupported assumptions.
- The required output format.

## Classification Categories

The lead agent classifies leads into:

- SOC
- Desktop
- VAPT
- Other

## Priority Levels

- Hot
- Warm
- Cold

## Important Prompt Rules

The AI should only use information provided in the lead.

It should not invent:

- Phone numbers
- Salary
- Budget
- Financial information
- Personal information
- Enrollment status
- Other facts that were not provided

## Structured Output

The model returns structured JSON containing:

- Category
- Priority
- Reason
- Recommended next action
- Draft reply

## Testing

I tested the classification system using 10 dummy leads.

Most classifications matched the expected result.

One lead produced a different priority classification, showing why AI systems should be evaluated instead of assuming every output is correct.

## Important Learning

A good AI application does not only require an LLM.

It also requires:

- Clear instructions
- Examples
- Output constraints
- Testing
- Evaluation

## Day 12 Deliverables

- Classification prompt
- Three input/output examples
- Structured JSON output
- 10 lead test results
- Expected vs AI classification comparison

## Status

COMPLETE