# Runbook usage

## Workspace

Follow [setup](../README.md#enter-the-workspace). `source ./shell/ops.zsh` enters interactive mode; `ops-leave` restores PATH, Python environment, history options, and prompt hooks. It does not change directories or clear case variables. Non-interactive sourcing does nothing.

| Override (export before entry) | Default |
| --- | --- |
| `OPS_VENV` | Checkout `.venv` |
| `OPS_HISTORY_FILE` | Checkout `.state/runbook-history` |

History is separate, not secret: commands and arguments are recorded. Entry can remain in normal history; third-party history plugins may keep their own logs. Avoid switching venvs or starting nested interactive shells while active. Re-entry does not stack modes; leave and re-enter after configuration changes.

The macOS launcher disables Terminal's session save/restore for its dedicated shell to avoid a second history store. Runbook history stays in `.state/` (or `OPS_HISTORY_FILE`); `ops-leave` restores the normal history path.

The bundled Starship profile is used only for this prompt. Existing prompt hooks remain active; the runbook prompt renders after them. Leaving removes only the runbook hook. Prompt rendering makes no network requests or file hashes.

## Execution

Runme execution is not currently supported. These runbooks assume a persistent interactive zsh session, including shell variables and interactive selection; Runme-specific session setup and block execution have not been adapted or verified. Use the terminal or the `run-runbook` Skill.

Follow the documented Steps. Headings may name the action directly or use Check / Act / Verify, separately or combined. These are review perspectives, not required sections; the responsibilities below still apply.

- Use documented code blocks intact where possible. If adapting them, preserve failure branches; a failed check must prevent dependent operations.
- Read each command before executing it. Keep inputs in one shell or explicitly pass them between invocations.
- Use task-specific variable names; zsh reserves names such as the read-only `status`.
- **Check:** inspect state and collect evidence. Downloads and evidence files may be saved here when their effects are stated.
- **Act:** perform the needed operation after reviewing targets and scope.
- **Verify:** observe the actual result, using bounded read-only retries for delayed completion.
- `READY` describes a particular check; it is not blanket approval. Stop on `STOP`; follow the stated branch on `DEFER` or `UNAVAILABLE`.
- Keep recovery and optional actions separate from the normal path. After interruption or a wrapper error, inspect actual results before retrying; the operation may already have completed.

Use short native commands or visible Python. Helpers print data or reports; do not automatically evaluate their output. Agents perform operational changes only within explicit authorization. Full metadata is for AI investigation, not a checklist humans must read line by line.

## Long code blocks

For agent execution, extract long blocks verbatim into temporary scripts using file tools, rather than pasting them into an interactive terminal. Preserve the whole block, including shell guards and heredoc delimiters.

- Check shell syntax with `zsh -n` before non-interactive execution. This does not check Python inside heredocs; syntax-check literal Python separately without executing it when needed.
- Set the documented working directory and pass required inputs explicitly, including arrays. Keep dependent commands in the same shell or transfer their outputs explicitly; child-shell assignments do not update the parent.
- Execute only the selected block and its necessary input setup, not the entire runbook. Remove temporary scripts afterward.
- If input is corrupted, stop dependent work and inspect actual files before retrying. Some operations may already have completed.

## AI assistance

See the [README](../README.md#use-the-skills) for Skill selection and CLI examples. Inputs and decision criteria come from the runbook; supply only overrides or narrower limits. The agent resolves its own environment rather than inheriting the operator's shell variables.

Execution uses `run-runbook`; explicitly requested improvements use `develop-runbook`. Unresolved decisions and failures stop execution unless the procedure provides a defer/skip branch. Required filesystem and network permissions must be available.

Direct path invocation uses this checkout's Skill. Installed plugin copies must be updated separately. For authoring rules, see the [policy](../plugins/runbook-ops/references/runbook-policy.md).

For Codex settings and network restrictions, consult the official [configuration reference](https://developers.openai.com/codex/config-reference) and [security documentation](https://developers.openai.com/codex/security).
