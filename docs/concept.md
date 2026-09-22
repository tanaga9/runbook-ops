# Living runbooks

## Why start with a runbook?

Turning a vague idea into automation is often harder than executing it. A runbook gives humans and AI a shared, executable document for aligning intent: start with one understandable action, observe the result, and refine the procedure together. A complete specification is not required.

The document accumulates useful procedural knowledge, not an execution transcript. Success means the observed result matches the user's purpose, not merely that a command exited successfully.

## From intent to automation

```text
Idea / conversation / optional Task brief
                 ↓
Runbook ↔ user execution ↔ observation ↔ correction with AI
                 ↓
Validated intent, decisions, and outcomes
                 ↓
Skill / rule-based script / continued runbook use
```

Choose a Skill when contextual judgment remains, a script when the rules are explicit and testable, or both. A one-off case can remain a runbook. Extract automation based on observed behavior and relevant exceptions rather than a polished document or one successful run.

The bundled authoring and execution Skills support this process; they are distinct from domain Skills developed later. Background Obsidian Notes can stay in their Vault, and an inbox brief is optional.

## What makes it useful?

The hypothesis is that trying understandable actions together reduces the effort from an idea to a useful procedure. Assess time to the first user-verified action, misunderstandings corrected, and decisions reusable without the whole conversation.

A Markdown execution engine, transaction guarantees, and a complete audit trail are outside this project's scope. See the [writing policy](../plugins/runbook-ops/references/runbook-policy.md) for document conventions and [design](design.md) for component responsibilities.
