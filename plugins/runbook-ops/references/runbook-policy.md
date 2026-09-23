# Runbook writing policy

A runbook is a procedure that humans and AI can both understand and carry out. Start with a rough goal, validate intent through actual results, and incorporate reusable lessons. Keep one Markdown file per case; reuse an existing case with the same goal and target. See [Concept](../../../docs/concept.md) for the development approach.

## Format and content

Use only `status: draft` or `status: ready` in YAML Front Matter, followed by one H1 title. Readiness describes the procedure, not execution progress, authorization, or current conditions.

- Include the goal, scope, case prerequisites, inputs, working directory, Steps, decision criteria, and necessary recovery.
- Use **Runbook → Step** as the hierarchy. Each Step completes a meaningful investigation, decision, or operation; name it by its purpose. Prefer verb + object headings, such as `Collect evidence` or `Choose a destination`, within each Step. Check / Act / Verify are also valid labels, not a required vocabulary.
- Keep references only where they help perform or understand the work. Never include secrets.
- Omit Outcome sections, usage dates, logs, transcripts, and per-run progress. Keep actual results and pending work in the conversation unless a separate log is requested.
- Treat shared usage conventions as known. Link them rather than repeating shell setup or detailed “How to use” sections. A brief AI instruction is enough: “AI agents: Use the `run-runbook` skill when working on this runbook.”
- Use plain English, short sentences, bullets for parallel points, and compact tables for conditions or comparisons. Before each code block, state its purpose and make the expected result and next action easy to find.

## Keep case logic visible

Keep target selection, judgment, operation order, effects, and verification understandable from the runbook itself.

- Prefer clear native commands and standard-tool pipelines. Use readable inline Python when shell branching, quoting, or structured data becomes cumbersome.
- Externalize only necessary bulky mechanics, such as format decoding. Explain the helper's inputs, outputs, responsibility, and limits; it must not hide case decisions or operational changes.
- Repository tests cover `src/` only. Validate individual runbooks with temporary checks when needed, without adding persistent case-specific tests.
- Declare case dependencies locally. Do not add domain commands, loaders, registries, compatibility layers, or package structure for a single case.
- Shared changes must solve an independent workspace or authoring problem. Promote case code only after demonstrated reuse across distinct cases and an explicit request for that shared capability.
- If the procedure becomes hard to review, split it at meaningful decisions or reduce scope. Do not conceal it in a whole-workflow executor merely to shorten the Markdown. Deliberate extraction into a Skill or script is appropriate after the behavior is validated.

For inline Python, show one understandable action or check with named intermediate values. Prefer the standard library; declare extra dependencies. Pass quoted shell arguments through a quoted heredoc (`python3 - "$input" <<'PY'`), never by interpolating values into Python source. Python cannot set parent-shell variables: use explicit shell assignments or branch on its exit status, not evaluation of generated code.

If a command-preparing helper is necessary, show the concrete command and its targets before execution. Preparation may inspect inputs but must not execute the operation or mutate its target. In human-led use, the operator reviews and executes the command; an Enter press is meaningful only when its effects are understood.

## Check / Act / Verify

| Review perspective | Responsibility |
| --- | --- |
| Check | Establish current state, inputs, and whether to proceed, skip, or stop |
| Act | Perform the needed operation within the authorized scope |
| Verify | Observe the result against explicit success criteria |

Use these perspectives to check completeness, not to impose headings or a fixed section sequence. Do not define Prepare, Select, or Decide as additional mandatory phases. Choose a natural structure for each Step:

- **Check only:** investigate, collect evidence, or resolve inputs without a main operational change.
- **Check / Act / Verify:** make the precondition, change, and result separately reviewable.
- **Purpose-based or combined headings:** use the action name alone when its responsibilities are clear, or merge related responsibilities under one heading when the unit remains understandable. Keep preconditions and success criteria explicit; do not merge across a required user decision or let failures fall through.

Do not add empty phases to satisfy a template. Make each Step's entry and completion conditions clear. Preserve the causal order of prerequisite checks, operations, and result verification regardless of headings. Steps may build on earlier results, but recheck changeable prerequisites before acting. When processing repeated items, state which Step restarts the cycle and which inputs must be refreshed.

Check may retrieve and save evidence when useful for the next decision. State network access, save locations, and effects; preserve existing files and validate retrieved data. Make the main operational change and its effects explicit regardless of the heading.

Keep the normal path executable in order. Place optional, deferred, and recovery actions in separate conditional sections with a trigger and return point. Keep immediate guards beside the operation they protect; finishing the normal path must not lead into recovery commands.

For delayed results, specify a wait interval, bounded retries, and a read-only check. Do not repeat a potentially non-idempotent operation just to see whether it succeeded. On interruption, inspect current state before retrying; prior commands and `ready` are not proof of completion.

## Choose code blocks by review boundaries

Each block should finish one understandable unit without making the operator manage mechanical intermediate state.

| Combine when no human decision intervenes | Keep separate |
| --- | --- |
| Decode, filter, and accept a unique match | Resolve ambiguity |
| Inspect existing evidence, fetch, retry, validate, and save | Accept a recommendation or expand scope |
| Resolve operation inputs and display their effects | Review targets before a consequential change |
| Collect evidence and print a concise summary | Optional AI inference and the final choice |

These are examples, not mandatory Steps. Neither one command per block nor one block per workflow is a target. Separate operations when each result needs review before the next.

Merged code must stop dependent operations on failure, clear stale state, clean up temporary files, and return a meaningful result. Printing `STOP` alone does not enforce a stop. Do not automate a decision merely to reduce block count.

## Show useful results and choices

- Print explicit outcomes such as `VERIFIED`, `STOP`, `NONE`, or `DEFER`, with the relevant target or reason. Humans should not need to read `$?`. Preserve useful native errors and machine-readable failure status.
- Distinguish no candidates, ambiguous matches, and inspection errors. Clear previous selections and recommendations before processing a new item.
- Verify effects, not just command exit codes: a skipped operation can return success. Prepared inputs are not completed operations.
- Show targets, a short recommendation, uncertainty, and the next choice. Keep detailed evidence available to AI or optional inspection instead of requiring humans to scan raw data or long inventories.
- Build choices from current available resources. Put a justified recommendation first; offer custom input where useful and allow defer/cancel without silently accepting a default. Use free text when candidates cannot be established.
- Keep labels separate from values, distinguish existing resources from proposed ones, and validate custom input. Selection alone does not create anything.
- Distinguish observed facts, mechanical hints, and AI recommendations; state uncertainty in conclusions even when the underlying data is verified. If inference is needed in a terminal, provide an actual invocation; prose alone does not run AI. Keep optional inference and its skip path explicit. Do not require humans to guess when they requested assistance.

## Scope and environment

Use repository paths relative to a stated working directory; resolve bundled resources from their location without private shell state or fixed checkout paths. Keep external work locations in case inputs and state platform/tool requirements.

Follow the execution project's applicable instructions. Honor separate source, target, and runbook locations, verify available access, and mark unresolved references as unconfirmed.

`develop-runbook` owns authoring; `run-runbook` owns execution. A request to execute a specified runbook through completion delegates its documented operations and decisions within the user's limits and existing access controls. Inspection or human-led requests remain narrower. Neither writing a runbook nor its readiness grants execution authority.

Agents use the current session rather than recursively launching Codex. Reconcile concurrent edits, preserve useful rationale, and improve the same procedure with lessons learned; execution alone does not change its status. If editing is blocked, report the proposed change rather than create a replacement elsewhere.
