---
name: develop-runbook
description: Create or improve a readable runbook from an idea, Note, conversation, or existing procedure. Use for authoring and incorporating lessons, not routine execution of a ready runbook.
---

# Develop a runbook

Read the [shared policy](../../references/runbook-policy.md). Keep domain logic in the case; ordinary authoring must not expand the shared foundation.

1. Resolve the goal, target project, references, and runbook path. Check for an existing procedure for the same case before creating one. A rough goal is enough; ask only questions that affect the next useful step.
2. Draft the smallest useful procedure: purpose, scope, inputs, and understandable Check / Act / Verify. Use `status: draft` while essential decisions remain unresolved. Keep commands visible; use inline Python or necessary adjacent support rather than an opaque workflow executor.
3. Work with the user to test intent against actual observations. Authoring permits document edits and requested investigation, not every operational change the draft proposes. For execution, follow `run-runbook` with the user's authorized scope.
4. Apply lessons directly to prerequisites, commands, decision criteria, and recovery. Keep usage dates, execution results, and logs out of the document. Preserve valid rationale and concurrent edits.
5. Review the draft against the authoring checks below. Mark `ready` when the procedure is sufficiently specified for its intended use; disclose untested parts in the conversation. Readiness is not evidence of past success or permission to execute.

Return the path, material improvements, remaining uncertainty, and next useful action. Do not require a complete questionnaire or add infrastructure for hypothetical reuse.

## Authoring checks

Use the shared policy's code-block and human-review guidance before handing over a new or edited runbook:

- Can the operator understand target selection, decisions, effects, and verification from the runbook itself? Remove unnecessary external case logic; do not add a framework or compatibility layer.
- Does each block finish a meaningful unit? Combine mechanical intermediate steps, but preserve user choices and consequential review boundaries. Make merged failures stop dependent work.
- Is the normal path executable in order without accidentally entering recovery? Give optional branches clear triggers, skip paths, and return points.
- Are inputs derived from current state, choices populated automatically, stale state cleared, and success/failure visible without reading shell exit codes?
- Does the human see only the information needed for the next decision? Keep detailed evidence available for AI without dumping it into routine output.
- Are explanations short, plain English, using bullets or compact tables? Keep status-only Front Matter and omit usage history.

Validate changed executable blocks with small temporary fixtures where behavior changed, including the relevant failure branch. Do not operate on real targets just to test authoring. Report what was tested and what remains untested in the conversation.

Use existing runbooks as examples of writing choices, not templates for required tools, data types, or Steps. Start each case from its own goal and smallest useful action.
