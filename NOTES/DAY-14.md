# Day 14 — Safe Personalized Replies

## Goal

Create safe, tailored draft responses for qualified leads, and ensure a human approves each reply before it is sent.

## Implementation

The Lead Agent is built with Python and Ollama.

No messages are sent automatically.

## Workflow

Lead
↓
AI Classification
↓
Reply Template
↓
AI Personalization
↓
Safety Guardrails
↓
Draft Reply
↓
Human Approval
↓
Yes → Approved for manual sending
No → Not sent

## Reply Features

- Reply templates organized by category
- Customized responses
- Lead details added when suitable
- Clear and professional replies
- Safety verifications
- Step requiring human approval

## Safety Guardrails

The agent is not allowed to fabricate or promise:

- Job placement
- Salary
- Discounts
- Certificates
- Internships
- Course policies
- Fees
- Other business details not supplied

## Human Approval

Each generated response needs:

HUMAN_APPROVED = Yes / No

If the answer is No, the response is not dispatched.

The system never sends messages automatically.

## Testing

Five unusual lead inquiries were assessed:

1. Normal course inquiry
2. Job guarantee request
3. Discount request
4. Salary guarantee request
5. Certificate and internship guarantee request

All five tests were completed successfully.

## Result

The Day 14 reply generation, safety checks, and human approval workflow all passed testing.