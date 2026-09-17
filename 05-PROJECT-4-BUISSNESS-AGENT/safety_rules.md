# Project 4 — Safety Rules

## Allowed Actions

The agent may automatically:

- Search FAQ information.
- Retrieve leads by status.
- Generate follow-up drafts.
- Read and process tool results.
- Log tool selections, results, and errors.

## Restricted Actions

The agent must NOT automatically:

- Send emails or messages.
- Delete leads or business data.
- Modify business records.
- Make irreversible changes.
- Publish content automatically.

## Human Confirmation

Human confirmation is required before:

- Sending an email or message.
- Deleting data.
- Updating business records.
- Performing any irreversible action.

## Error Handling

If a tool fails:

1. Record the error in the agent log.
2. Do not pretend the tool succeeded.
3. Return a clear failure message to the user.
4. Stop the affected operation safely.

## Tool Call Limit

The agent must enforce a maximum number of tool calls for a single request.

Current maximum:

3 tool calls.

## Observability

The agent should log:

- User request.
- Selected tool.
- Tool arguments.
- Tool result.
- Error information when a failure occurs.